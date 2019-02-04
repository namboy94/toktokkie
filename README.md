# toktokkie

|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namibsun/python/toktokkie/badges/master/build.svg)](https://gitlab.namibsun.net/namibsun/python/toktokkie/commits/master)|[![build status](https://gitlab.namibsun.net/namibsun/python/toktokkie/badges/develop/build.svg)](https://gitlab.namibsun.net/namibsun/python/toktokkie/commits/develop)|

![Logo](resources/logo/logo-readme.png)

The toktokkie media manager consists of a collection of command-line tools used
for keeping track of media.

Currently, the following media types are supported:

- Book
- Book Series
- Movie
- TV Series

## Structure

The metadata for a Media directory is stored inside the ```.meta```
subdirectory in a file called ```info.json```. Additionally, folder icons may
be stored in ```.meta/icons```.

## Generating and modifying metadata

To generate metadata for a media directory, use the
```toktokkie-metadata-gen``` script.

To modify the metadata afterwards, you can use the
```toktokkie-metadata-add``` script.

## Further Information

* [Changelog](CHANGELOG)
* [License (GPLv3)](LICENSE)
* [Gitlab](https://gitlab.namibsun.net/namibsun/python/toktokkie)
* [Github](https://github.com/namboy94/toktokkie)
* [Progstats](https://progstats.namibsun.net/projects/toktokkie)
* [PyPi](https://pypi.org/project/toktokkie)
