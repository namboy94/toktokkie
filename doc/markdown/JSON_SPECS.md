JSON Specs

The Media Directory metadata information is held via the `info.json` file in the `.meta` directory.

There are various classes of Media Types. They share various traits. The required traits are
marked with `+`, the optional ones with `*`. The type of value that should be entered for that key is
represented after the colon(`:`). Parent media types are indicated using `<=`.

    media:                 # media is essentially an abstract media type. Base for all other media types
        + type: string     # the media type (like 'tv_series' or 'ebook')
        + name: string     # The name of the media contained within here
        + tags: List[str]  # A list of tags for this media
    
    tv_series <= media:
        + resolutions: List[Tuple[int, int]]  # A list of resoultions contained within this tv series directory
        + audio_langs: List[str]              # A list of audio languages, denoted as 3-character capital terms
                                              # (i.e. ENG, GER, JAP, etc.)
        + subtitle_langs: List[str]           # A list of subtitle languages, denoted as 3-character capital terms
                                              # (i.e. ENG, GER, JAP, etc.)
        * tvdb_url: str                       # Link to the series' thetvdb.com page
        * seasons: Dict[str, Dict[str, any]]  # Can be used to overwrite any of the series' data for one particular
                                              # season. Seasons inherit all traits from the series implicitly,
                                              # differences have to be provided here explicitly
    
    anime_series <= tv_series:
        * myanimelist_url  # An URL to the anime's myanimelist.net page. Can also be overridden using seasons
        
    ebook <= media:
        + author: string  # The book's author
        + isbn: string    # The book's ISBN. Not all ebooks have ISBNs though, in which case this value will be null
    
    light_novel <= ebook:
        * myanimelist_url: string   # A URL to the novel's myanimelist page
        * novelupdates_url: string  # A URL to the novel's novelupdates page
        + official: boolean         # Indicates if this is the offical translation or not
        
    music:
        + artist: string
        * featuring: string
        
All media type names should be singular (e.g. not ebooks, but ebook. tv_series is singular here)