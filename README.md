#Parmesan

1. [About Parmesan](#about-parmesan)
2. [Installation Instructions](#installation-instructions)
3. [Configuration Instructions](#configuration-instructions)
4. [Usage Instructions](#usage-instructions)
5. [Troubleshooting](#troubleshooting)

##About Parmesan
Parmesan automates the process of running your MultiMarkdown (or similar) parser on the content of your website, and places that content in template html files. Just write some content in markdown, save the file in the location you want it on your website, and run parm. It's that easy.

I tried [Jekyll](http://jekyllrb.com/) and I tried [MultiMarkdown-CMS](https://github.com/fletcher/MultiMarkdown-CMS), but neither really fit my needs. Jekyll lacks MultiMarkdown support, and even MultiMarkdown-CMS has more complex features than I wanted. I wanted to be able to make a template for my index and a template for articles and then just write content. I didn't need to let people comment or log in. I just wanted a static site generation tool, so I wrote Parmesan.

Why 'Parmesan'? Because __P__ (ython) (MultiM) __ar__ (kdown) __m__ (anagement)... something. I just like the name.

##Installation Instructions
Just clone Parmesan into the root of whatever portion of your website you want to manage. The .parm folder should be in the root directory.

##Configuration Instructions
The default settings file is `.parm/default.parm-settings`. If you need to override any of these settings, it is reccomended that you create the file `.parm/user.parm-settings`, and add the options you would like to override.
####Options
| Option | Values | Description |
| --- | --- | --- |
| parser | multimarkdown, markdown, pandoc, etc. | The parser you want to use. Can be anything. (default: multimarkdown) |
| parse_syntax | `$file > $out` | The syntax for your chosen parser. $file and $out are required. Will be called as `<parser> <parse_syntax>` |
| generate_txt_version | true, false | If true, will generate .txt file versions of your markdown that can be viewed on the web. (default: false)|
| include_html_in_txt | true, false | If true and `generate_txt_version` is true, the html template code will be included as well as the markdown text when creating the optional .txt files. (default: false) |


##Usage Instructions
