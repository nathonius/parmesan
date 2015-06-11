#Parmesan

1. [About Parmesan](#about-parmesan)
2. [Installation Instructions](#installation-instructions)
3. [Configuration Instructions](#configuration-instructions)
    1. [Configuration Settings](#configuration-settings)
    3. [Templates](#templates)
4. [Usage Instructions](#usage-instructions)
    1. [Content Format](#content-format)
    2. [Template Format](#template-format)
5. [Troubleshooting](#troubleshooting)

##About Parmesan
Parmesan automates the process of running your MultiMarkdown (or similar) parser on the content of your website, and places that content in template html files. Just write some content in markdown, save the file in the location you want it on your website, and run parm. It's that easy.

I tried [Jekyll](http://jekyllrb.com/) and I tried [MultiMarkdown-CMS](https://github.com/fletcher/MultiMarkdown-CMS), but neither really fit my needs. Jekyll lacks MultiMarkdown support, and even MultiMarkdown-CMS has more complex features than I wanted. I wanted to be able to make a template for my index and a template for articles and then just write content. I didn't need to let people comment or log in. I just wanted a static site generation tool, so I wrote Parmesan.

Why 'Parmesan'? Because __P__ (ython) (MultiM) __ar__ (kdown) __m__ (anagement)... something. I just like the name.

##Installation Instructions
Just clone Parmesan into the root of whatever portion of your website you want to manage. The .parm folder should be in the root directory. Alternatively, you can set a root directory in the config file or at the command line.

Requires python 3.2 or higher.

##Configuration Instructions
The settings file is `.parm/parm-settings.cfg`.

####Configuration Settings
These are the options that can be used in `parm-settings.cfg`, and what they mean. Most can be overridden at the command line.

| Option | Values | Description |
| --- | --- | --- |
| verbose | true, false | By default parmesan gives very little output. Set to true for more. |
| parser | multimarkdown, markdown, pandoc, etc. | The parser you want to use. Can be anything. (default: multimarkdown) |
| file_types | list of file types beginning with `.` | These are the types of files parmesan looks for when generating content. |
| root_path | any path to your website | Sets the default directory for the website to process. |
| default_template | the filename (not path) of the default template to use | Used when no template is specified in the content file. |

####Templates
Templates are files stored in `.parm/templates`. The html generated from your content files is inserted into these where marked with `<parm></parm>` Templates can be named whatever you would like, but the file type must match the intended filetype (ie. html, htm, php). It would make sense to name these based on what they are used for: index.html, article.html, post.html, about.html, contact.html, etc.

##Usage Instructions
Using parmesan is as easy as typing `python parm.py <dir>` in the `.parm` directory. The `<dir>` argument can be omitted if `root_path` is specified in `parm-settings.cfg`. There are also some additional flags and options you can specify as well, all of which override the same setting in `parm-settings.cfg`.

| Short Flag | Long Form Flag | Value | Description |
| --- | --- | --- | --- |
| -v | --verbose | N/A | Verbose mode. More output. |
| -p | --parser | any installed parser that takes a file path as input and returns the output to the terminal | Used to specify which markup language parser to use. |
| -t | --types | file types for parm to consider | Overrides setting in `parm-settings.cfg` |
| -f | --force | N/A | Force parsing of all content files, even if they haven't been modified. Useful if templates have changed. |

####Content Format
Parmesan looks for a certain format at the top of content files. This is not required if you have specified a default template. The format is a custom XML tag: `<parm>template_name.html</parm>`  

####Template Format
The parmesan syntax for templates is similar to the syntax for content. In your template add `<parm></parm>` where your content should be placed. Nothing is necessary between the tag, but both tags must be present (so an XML singleton `<parm/>` would not work).

Otherwise, templates are just html/php files. They can include as much or as little frills as you want. CSS, javascript, everything should work as normal.  
Warning: Do be careful about file paths. Don't make the javascript or css paths relative to the template file, but relative to where the content file is.

##Troubleshooting
If you have an issue or question just submit it here.