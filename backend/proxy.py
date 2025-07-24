import httpx
from urllib.parse import urlencode
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from xml.dom.minidom import Element
import xml.etree.ElementTree as ET
from typing import Any
from collections import defaultdict
import click
import uvicorn



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



async def proxy_request(request: Request, srv_url: str):
    """Leitet eine Anfrage an den MediaServer weiter."""
    raw_path = request.url.path
    request_path = "/" + "/".join(filter(None, raw_path.split("/")))
    
    query_params = dict(request.query_params)
    convert_to_json = "json" in query_params
    if convert_to_json:
        query_params.pop("json")
    
    query_string = urlencode(query_params).encode('utf-8')
    url = httpx.URL(path=request_path, query=query_string)
    headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}
    
    async with httpx.AsyncClient(base_url=srv_url) as client:
        try:
            rp = await client.request(
                method=request.method, url=url, headers=headers,
                content=await request.body(), timeout=20.0
            )
            
            response_headers = {
                k: v for k, v in rp.headers.items() 
                if k.lower() not in ['transfer-encoding', 'content-encoding', 'content-length']
            }
            response_headers["Content-Length"] = str(len(rp.content))
            
            if convert_to_json and "xml" in rp.headers.get("content-type", ""):
                try:
                    json_content = xmltodict(rp.content.decode("utf-8", errors="ignore"))
                    return JSONResponse(content=json_content, status_code=rp.status_code)
                except Exception as e:
                    return JSONResponse(
                        content={"error": "Failed to convert XML to JSON", "details": str(e)},
                        status_code=500
                    )
            else:
                return Response(
                    content=rp.content,
                    status_code=rp.status_code,
                    headers=response_headers,
                    media_type=rp.headers.get("content-type")
                )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Proxy request failed", "details": str(e)},
                status_code=502
            )

def create_app(srv_url: str) -> FastAPI:
    """Erstellt die FastAPI-App mit konfigurierter SRV_URL"""
    app = FastAPI(
        title="MediaServerAPI Proxy",
        description="Ein validierender Proxy für die DVBViewer Media Server API.",
        version="0.3.0",
    )
    
    @app.api_route("/{path:path}", methods=["GET", "POST", "HEAD", "PUT", "DELETE", "PATCH"])
    async def catch_all_proxy(request: Request):
        return await proxy_request(request, srv_url)
    
    return app

@click.command()
@click.option('--srv-url', default='http://localhost:8089', help='URL des MediaServers')
@click.option('--host', default='0.0.0.0', help='Host-Adresse des Proxys')
@click.option('--port', default=8000, help='Port des Proxys', type=int)
def run(srv_url: str, host: str, port: int):
    """Startet den Proxy-Server mit konfigurierbaren Parametern"""
    app = create_app(srv_url)
    print(f"Starting proxy server on {host}:{port}")
    print(f"Proxying requests to: {srv_url}")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run()