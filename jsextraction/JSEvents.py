class JSEvents:
    EVENTS = [
        "onafterprint", "onbeforeprint", "onbeforeunload", "onerror", "onhaschange", "onload", "onmessage", "onoffline", "onpagehideden", "onpageshow", "onpopstatey", "onredo", "onresize", "onstorage", "onundo", "onunload", "onblur", "onchange",
        "oncontextmenu", "onfocus", "onformchange", "onforminput", "oninput", "oninvalid", "onreset", "onselect", "onsubmit", "onkeydown", "onkeypress", "onkeyup", "onclick", "ondblclick", "ondragenter", "ondragleave", "ondragover", "ondragstart",
        "ondrop", "onmousedown", "onmousemovem", "onmouseout", "onmouseover", "onmouseup", "onmousewheeled", "onscroll", "onabort", "oncanplay", "oncanplaythrough", "ondurationchange", "onemptied", "onended", "onerror", "onloadeddata", "onloadedmetadata", 
        "onloadstart", "onpause", "onplay", "onplaying", "onprogress", "onratechange", "onreadystatechange", "onseeked", "onseekingg", "onstalled", "onsuspendaded", "ontimeupdate", "onvolumechange", "onwaiting"
    ]    

    def get_select_format(self) -> str:
        events_str = ""
        events_str += ", ".join(f"[{event}]" for event in self.EVENTS)
        return events_str