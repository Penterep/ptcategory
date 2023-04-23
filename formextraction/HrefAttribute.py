class HrefAttribute:
    NOT_FILE_SUFFIXES = ["php", "js", "css", "html", "asp", "aspx", "pl", "jsp", "py", "xhtml"]
    SPECIAL_PREFIXES = ("mailto", "tel")
    WEB_SUFFIXES = ["ac", "ac.uk", "ad", "ae", "aero", "af", "ag", "ai", "al", "am", "an", "ao", "aq", "ar", "arpa", "as", "asia", "at", "au", "aw", "ax", "az", "ba", "bb", "bd", "be", "bf", "bg", "bh", "bi", "biz", "bj", "bm", "bn", "bo", "br", "bs", "bt", "bv", "bw", "by", "bz", "ca", "cat", "cc", "cd", "cf", "cg", "ch", "ci", "ck", "cl", "cm", "cn", "co", "co.uk", "com", "coop", "cr", "cs", "cu", "cv", "cw", "cx", "cy", "cz", "dd", "de", "dj", "dk", "dm", "do", "dz", "ec", "edu", "ee", "eg", "eh", "er", "es", "et", "eu", "fi", "firm", "fj", "fk", "fm", "fo", "fr", "fx", "ga", "gb", "gd", "ge", "gf", "gg", "gh", "gi", "gl", "gm", "gn", "gov", "gov.uk", "gp", "gq", "gr", "gs", "gt", "gu", "gw", "gy", "hk", "hm", "hn", "hr", "ht", "hu", "id", "ie", "il", "im", "in", "info", "int", "io", "iq", "ir", "is", "it", "je", "jm", "jo", "jobs", "jp", "ke", "kg", "kh", "ki", "km", "kn", "kp", "kr", "kw", "ky", "kz", "la", "lb", "lc", "li", "lk", "lr", "ls", "lt", "ltd.uk", "lu", "lv", "ly", "ma", "mc", "md", "me", "me.uk", "mg", "mh", "mil", "mk", "ml", "mm", "mn", "mo", "mobi", "mod.uk", "mp", "mq", "mr", "ms", "mt", "mu", "museum", "mv", "mw", "mx", "my", "mz", "na", "name", "nato", "nc", "ne", "net", "net.uk", "nf", "ng", "nhs.uk", "ni", "nl", "no", "nom", "np", "nr", "nt", "nu", "nz", "om", "org", "org.uk", "pa", "pe", "pf", "pg", "ph", "pk", "pl", "plc.uk", "pm", "pn", "post", "pr", "pro", "ps", "pt", "pw", "py", "qa", "re", "ro", "rs", "ru", "rw", "sa", "sb", "sc", "sch.uk", "sd", "se", "sg", "sh", "si", "sj", "sk", "sl", "sm", "sn", "so", "sr", "ss", "st", "store", "su", "sv", "sy", "sz", "tc", "td", "tel", "tf", "tg", "th", "tj", "tk", "tl", "tm", "tn", "to", "tp", "tr", "travel", "tt", "tv", "tw", "tz", "ua", "ug", "uk", "um", "us", "uy", "uz", "va", "vc", "ve", "vg", "vi", "vn", "vu", "web", "wf", "ws", "xxx", "ye", "yt", "yu", "za", "zm", "zr", "zw"]
    
    def __init__(self, value:str) -> None:
        self.value = value
        
    # Determines if the href is a file or not
    def is_file_href(self) -> bool:
        if self.value.startswith(self.SPECIAL_PREFIXES):
            return False
        
        suffix = self.get_suffix()
        return not suffix == "" and not suffix in self.NOT_FILE_SUFFIXES and not suffix in self.WEB_SUFFIXES
    
    # Determines if the href is a web link or not
    def get_suffix(self) -> str:
        last_slash_part = self.get_last_slash_part()
        split_by_dot = last_slash_part.split(".")
        if len(split_by_dot) > 1:
            return split_by_dot[-1]
        else:
            return ""
    
    # Returns the last part of the href after the last slash
    def get_last_slash_part(self) -> str:
        parts = self.get_value_without_params().split("/")
        return parts[-1]
    
    # Returns the href without any parameters
    def get_value_without_params(self) -> str:
        value_without_params = self.strip_from_character(self.value, "?")
        return self.strip_from_character(value_without_params, "#")
        
    # Strips the string from the first occurence of the character
    def strip_from_character(self, s: str, character:str) -> str:
        stripped = s
        character_index = stripped.find(character)
        if character_index != -1:
            stripped = stripped[character_index:]
        return stripped