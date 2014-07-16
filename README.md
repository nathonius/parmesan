#Parmesan

1. [About Parmesan](#about-parmesan)
2. [Installation Instructions](#installation-instructions)
3. [Configuration Instructions](#configuration-instructions)
    1. [Default Options](#default-options)
    2. [Additional Options](#additional-options)
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
Just clone Parmesan into the root of whatever portion of your website you want to manage. The .parm folder should be in the root directory.

##Configuration Instructions
The default settings file is `.parm/default.parm-settings`. If you need to override any of these settings, it is reccomended that you create the file `.parm/user.parm-settings`, and add the options you would like to override.
####Default Options
These are the options in `default.parm-settings`, and what they mean.

| Option | Values | Description |
| --- | --- | --- |
| parser | multimarkdown, markdown, pandoc, etc. | The parser you want to use. Can be anything. (default: multimarkdown) |
| parse_syntax | Example: `$file > $out` | The syntax for your chosen parser. `$file` and `$out`, the input file and the output file respectively, are required. Will be called as `<parser> <parse_syntax>` (default: multimarkdown syntax) |
| generate_txt_version | true, false | If true, will generate .txt file versions of your markdown that can be viewed on the web. (default: false)|
| include_html_in_txt | true, false | If true and `generate_txt_version` is true, the html template code will be included as well as the markdown text when creating the optional .txt files. (default: false) |

####Additional Options
These options can be added to `user.parm-settings`, but are not present in `default.parm-settings`.

| Option | Values | Description |
| --- | --- | --- |
| default_template | `template.html` | Default template to use if none specified. Can be any template inside `.parm/templates` |

####Templates
Templates are files stored in `.parm/templates`. The html generated from your content files is inserted into these where marked with `{{content-here}}` or `{{content-id: <id>}}` if you have more than one content section for a template. These can be named whatever you would like, but the file type must match the intended filetype (ie. html, htm, php). It would make sense to name these based on what they are used for: index.html, article.html, post.html, about.html, contact.html, etc.

##Usage Instructions
Using parmesan is as easy as typing `python parm.py` in the top directory (the directory that contains `.parm`). There are also some additional flags and options you can specify as well.

| Flag | Value | Description |
| --- | --- | --- |
| -v | N/A | Verbose mode. Essentially prints the log to the terminal. (default: off) |

####Content Format
Parmesan looks for a certain format at the top of content files. This is not required if you have specified a default template. The format is a modified JSON syntax:
```
{{
    "template": "post.html",
    "content-id": "post-body"
}}
```

This block of parmesan specific code can also show up again later in your content document if you have more than one place in your template to put content. For example:
```
{{
    "template": "post.html",
    "content-id": "post-header"
}}

<CONTENT>

{{
    "content-id": "post-body"
}}

<CONTENT>

{{
    "content-id": "post-summary"
}}

<CONTENT>
```

Then if the content-id is specified in the given template, the content following the content-id declaration will be appropriately placed.

| Variable | Value | Description |
| --- | --- | --- |
| template | Any template in `.parm/templates` | Specifies the template to use. Only the first template declaration will be used. Further declarations are ignored. Required if a default template is not set. |
| content-id | Any specified `{{content-id: <id>}}` section in a template file | Tells parmesan where in the template file to place your content. Not required if template only has `{{content-here}}`. |

Note: If you want parmesan to ignore a block of parmesan syntax and include it in your content, place the following html comment just above the syntax block. 
`<!--parmesan-ignore-->`

####Template Format
The parmesan syntax for templates is similar to the syntax for content. In your template add `{{content-here}}` where your content should be placed. Or, if you have more than one section, add `{{content-id: <id>}}`, where `<id>` is the same as specified in a content document.

Otherwise, templates are just html/php files. They can include as much or as little frills as you want. CSS, javascript, everything should work as normal.  
Warning: Do be careful about file paths. Don't make the javascript or css paths relative to the template file, but relative to where the content file is.