#!/usr/bin/env python3
import argparse
import json
import os.path as path
import os
import subprocess
import re


def main():
    arg_parser = argparse.ArgumentParser()
    # All arguments can be set in parm-settings.cfg, but these take priority
    arg_parser.add_argument('root_path',
                            help='Root path of the site. By default this is one directory above this file.',
                            default=None)
    arg_parser.add_argument('-v', '--verbose', help='Make output verbose', dest='verbose', action='store_true',
                            default=False)
    arg_parser.add_argument('-p', '--parser', help='Select a different parser. Default is multimarkdown.',
                            dest='parser', default=None)
    arg_parser.add_argument('-t', '--types',
                            help='File types to consider. Default is .mmd files. List as many as needed.',
                            dest='file_types', nargs='*', default=None)
    arg_parser.add_argument('-f', '--force', help='Force recreating all files, even if they have not been modified.',
                            action='store_true', dest='force', default=False)
    args = arg_parser.parse_args()

    # Read options and args into parameters
    parameters = get_parameters(args)

    # Read Manifest
    manifest = read_manifest(parameters)

    # Now go through each file in the root
    modified = []
    for root, dirs, files in os.walk(parameters["root_path"]):
        # Skip hidden dirs
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        # Check each file
        for name in files:
            file_path = path.join(root, name)
            # Skip the file if it's not a content file
            if not is_content(file_path, parameters):
                continue
            # Skip the file if it hasn't been modified since last look
            if file_path in manifest.keys() and path.getmtime(file_path) == manifest[file_path] and not parameters[
                "force"]:
                continue

            if parameters["verbose"]:
                print("Processing " + name)
            # Run parser on file - returns tuple of (content, template_path)
            content, template_path = parse(file_path, parameters)

            if parameters["verbose"]:
                print("\tFile parsed. Got template " + template_path)
            # Find template, splice in new content. Returns the content of the output file and the path to write to.
            out, out_path = produce(content, template_path, file_path, parameters)

            if parameters["verbose"]:
                print("\tNew file ready for writing. Writing " + out_path)
            # Write the new file
            with open(out_path, 'w') as fp:
                fp.write(out)

            if parameters["verbose"]:
                print("\tFile written. Updating manifest and continuing.")
            # Now update the manifest
            manifest[file_path] = path.getmtime(file_path)
            modified.append(file_path)

    # Checked all files, write new manifest
    write_manifest(parameters, manifest)

    # Clean up temp file
    if path.isfile(parameters["temp_file_path"]):
        os.remove(parameters["temp_file_path"])

    # Done, give some output.
    print("Done. Processed " + str(len(modified)) + " files.")
    if parameters["verbose"]:
        for file_path in modified:
            print("\t" + path.basename(file_path))


def is_content(file_path, params):
    """Checks given file against file types specified in parm-settings.cfg"""
    for file_type in params["file_types"]:
        if file_path.endswith(file_type):
            return True
    return False


def produce(content, template_path, file_path, params):
    """Returns the fully developed html and the path to save it."""
    # If template_path is None, that means that we are using the default template
    if not template_path:
        template_path = path.join(params["parm_path"], "templates")
        template_path = path.join(template_path, params["default_template"])

    # Check and make sure the template exists
    if not path.isfile(template_path):
        raise FileNotFoundError("Could not locate template " + template_path)

    # Read the template
    with open(template_path, 'r') as fp:
        template = fp.read()

    # Is there a <parm></parm> tag?
    content_spec = re.search(r"<parm>.*</parm>", template)
    if not content_spec:
        raise ValueError("Could not locate <parm> tag in template.")
    # Replace it!
    output = re.sub(r"<parm>.*</parm>", content, template, count=1)

    # Figure out what the output file path should be based on template type and content path
    output_path = file_path[:file_path.rfind('.')]
    output_path += template_path[str(template_path).rfind('.'):]

    # Send it all back
    return output, output_path


def parse(file_path, params):
    # Read file
    with open(file_path, 'r') as fp:
        markdown = fp.read()
        # Look for <parm>template.html</parm> tag
        template_spec = re.search(r"<parm>.*</parm>", markdown)
        check_template = None
        if not template_spec and "default_template" not in params.keys():
            raise ValueError("No default template specified and could not find template spec in " + file_path)
        else:
            # Replace the first occurrence of <parm></parm> with empty string
            markdown = re.sub(r"<parm>.*</parm>", "", markdown, count=1)
            # Now extract the template and if available
            template = re.split(r"<.*?>", template_spec.group(0))[1]
            # Does the template exist?
            check_template = path.join(params["parm_path"], "templates")
            check_template = path.join(check_template, template)
            if not path.isfile(check_template):
                raise FileNotFoundError("Could not locate template " + check_template)

    # Run parser
    with open(params["temp_file_path"], 'w') as fp:
        fp.write(markdown)
    syntax = [params["parser"], params["temp_file_path"]]
    content = str(subprocess.check_output(syntax).decode('utf-8'))
    return content, check_template


def get_parameters(cli_args):
    """cli_args is a Namespace object, so just a blank class. Running vars(args) returns a
    dictionary of attributes and values. The goal of this function is to read in options
    from the config file and command line, with cli args taking priority."""
    cli_args = vars(cli_args)
    # Get path to config file
    parm_path = path.dirname(__file__)
    cfg_path = path.join(parm_path, "parm-settings.cfg")
    if not path.isfile(cfg_path):
        raise FileNotFoundError("parm-settings.cfg not found")

    # Open the config file
    parameters = None
    with open(cfg_path, 'r') as fp:
        try:
            parameters = json.load(fp)
        except ValueError:
            raise ValueError("Could not decode parm-settings.cfg. Check json format.")
    # Overwrite any params present in both the config file and cli args
    for value in cli_args.keys():
        if not cli_args[value] is None:
            parameters[value] = cli_args[value]
    # Add the base path of the .parm folder to the parameters and path to site root, useful in many places
    parameters["parm_path"] = parm_path
    parameters["temp_file_path"] = path.join(parameters["parm_path"], "temp.mmd")
    if not cli_args["root_path"] and "root_path" not in parameters.keys():
        parameters["root_path"] = path.dirname(parm_path)

    return parameters


def read_manifest(params):
    """Reads the json manifest, formats it into a dictionary with the form file_path : modified,
    where modified is the last modified date of the file."""
    manifest_path = path.join(params["parm_path"], "manifest.json")
    if not path.isfile(manifest_path):
        raise FileNotFoundError("manifest.json not found")

    # Open the manifest
    manifest = None
    with open(manifest_path, 'r') as fp:
        try:
            manifest = json.load(fp)
        except ValueError:
            raise ValueError("Could not decode manifest.json. Check json format.")

    return manifest


def write_manifest(params, manifest):
    """Given the dictionary form of the manifest, formats it back into json and writes it."""
    manifest_path = path.join(params["parm_path"], "manifest.json")
    if not path.isfile(manifest_path):
        raise FileNotFoundError("manifest.json not found")

    # Open the manifest for writing
    with open(manifest_path, 'w') as fp:
        try:
            formatted_manifest = json.dumps(manifest)
            fp.write(formatted_manifest)
        except:
            raise ValueError("Could not write new manifest. Check json format of manifest dictionary.")


if __name__ == "__main__":
    main()
