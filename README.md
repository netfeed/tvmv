# tvmv

tvmv is a tool for renaming TV-files into another scheme. For example to fit with the naming structur of [Plex](https://support.plex.tv/hc/en-us/articles/200220687-Naming-Series-Season-Based-TV-Shows). tvmv is not opinionated and you should be able to rename the file to pretty much whatever you want.

## Format

The -f/--format flag can use these arguments:

* show 
* season 
* episode
* episode_title

More can be added if needed.

season/episode can also be zero padded with:

    season.pad(2)

To use the arugments in a format string you'll need to embed them in a pair of {}

    {show}/Season {season.pad(2)}/{show} - s{season.pad(2)}e{episode.pad(2)} - {episode_title}

Which would result in something like:

    A Show/Season 01/A Show - s01e03 - The fancy episode

tvmv will try to take as much information as possible from the file path, but there's a special case when episode_title is used. From that point we will try to get information from [tvrage](http://services.tvrage.com/). If we succeed, then we'll use the episode title *and* the show title from the information we get. So "Bobs Burgers", would become "Bob's Burgers" for example.

## Todo

* use more information from tvrage and cache that for fewer requests (for example nextepisode)
* user-agent for tvrage requests

## License

    Copyright (c) 2015 Victor Bergöö

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
