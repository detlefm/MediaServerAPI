from xml.dom.minidom import Element
import xml.etree.ElementTree as ET
from typing import Any
from collections import defaultdict


def xmltodict(xml: str | list[str]) -> dict[str, Any]:
        """Converts an xml tree to dict
        Args:
            xml (str | list): xml string or list of strings
        Returns:
            dict: dictionary
        """

        def __to_dict(t: Element) -> dict[str, Any]:
            d = {t.tag: {} if t.attrib else None}  # type: ignore
            if children := list(t):  # type: ignore
                dd = defaultdict(list)
                for dc in map(__to_dict, children):
                    for k, v in dc.items():
                        dd[k].append(v)
                d = {
                    t.tag: {  # type: ignore
                        k: v[0] if len(v) == 1 else v for k, v in dd.items()
                    }
                }

            if t.attrib:  # type: ignore
                d[t.tag].update((k, v) for k, v in t.attrib.items())  # type: ignore

            if t.text:  # type: ignore
                text = t.text.strip()  # type: ignore
                if children or t.attrib:  # type: ignore
                    if text:
                        d[t.tag]["#text"] = text  # type: ignore
                else:
                    d[t.tag] = text  # type: ignore
            return d

        txt = xml if isinstance(xml, str) else "".join([t.strip() for t in xml])
        return __to_dict(ET.fromstring(txt))  # type: ignore        

