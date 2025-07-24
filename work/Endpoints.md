Hier ist eine gruppierte Liste der API-Endpunkte aus den Dokumenten, inklusive der als "deprecated" markierten Endpunkte und `curl`-Beispielaufrufen.

---

### **1. Status Informationen**
- **`/api/version.html`**  
  - Beschreibung: Gibt die Version des Media Servers zurück, inkl. Instanznummer (ab Media Server 3.3.1).  
  - Attribute: `iver` (Version als Integer), `inst` (Instanznummer).
  - **Beispielaufruf (curl):**
    ```bash
    # Standard-XML-Antwort
    curl http://localhost:8000/api/version.html
    # JSON-Antwort anfordern
    curl "http://localhost:8000/api/version.html?json=1"
    ```

- **`/api/status2.html`**  
  - Beschreibung: Liefert detaillierte Statusinformationen (Timer, Aufnahmen, Rechte, EPG-Status, etc.).  
  - Ersetzt: `/api/status.html` (deprecated).
  - **Beispielaufruf (curl):**
    ```bash
    # Standard-XML-Antwort
    curl http://localhost:8000/api/status2.html
    # JSON-Antwort anfordern
    curl "http://localhost:8000/api/status2.html?json=1"
    ```

- **`/api/epgstatus.html`**  
  - Beschreibung: Gibt EPG-spezifische Statusinformationen zurück (Sprache, Zeitzone, Importstatus, etc.).
  - **Beispielaufruf (curl):**
    ```bash
    # Standard-XML-Antwort
    curl http://localhost:8000/api/epgstatus.html
    # JSON-Antwort anfordern
    curl "http://localhost:8000/api/epgstatus.html?json=1"
    ```

---

### **2. Konfiguration und Dateien**
- **`/api/getconfigfile.html`**  
  - Beschreibung: Lädt Konfigurationsdateien (z.B. `service.xml`) herunter.  
  - Parameter: `file` (Pfad relativ zum Konfigurationsordner).
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/getconfigfile.html?file=config%5Cservice.xml"
    ```

- **`/api/setting.html`**  
  - Beschreibung: Liest Einstellungen aus der `service.xml`.  
  - Parameter: `sec` (Sektion), `id` (Einstellungs-ID), `def` (Standardwert).
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/setting.html?sec=WebGeneral&id=StreamPort&def=7522"
    ```

- **`/api/store.html`**  
  - Beschreibung: Key-Value-Speicher für Add-On-Einstellungen.  
  - Aktionen: `read`, `write`, `delete`, `updatefile`.
  - **Beispielaufruf (curl):**
    ```bash
    # Wert schreiben
    curl "http://localhost:8000/api/store.html?action=write&sec=myaddon&key=setting1&value=somevalue"
    # Wert lesen
    curl "http://localhost:8000/api/store.html?action=read&sec=myaddon&key=setting1"
    ```

---

### **3. Kanalliste und Favoriten**
- **`/api/getchannelsxml.html`**  
  - Beschreibung: Liefert die Kanalliste als XML.  
  - Filterparameter: `rootsonly`, `group`, `id`, `logo`, `rtsp`, `tvonly`, `radioonly`, etc.
  - **Beispielaufruf (curl):**
    ```bash
    # Nur TV-Kanäle mit Logos anfordern
    curl "http://localhost:8000/api/getchannelsxml.html?tvonly=1&logo=1"
    # Als JSON anfordern
    curl "http://localhost:8000/api/getchannelsxml.html?tvonly=1&logo=1&json=1"
    ```

- **`/api/getlogoassignment.html`**  
  - Beschreibung: Gibt Logo-Zuordnungen für Kanäle zurück.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/getlogoassignment.html?name=Das%20Erste%20HD"
    ```

---

### **4. Medien und Aufnahmen**
- **`/api/mediafiles.html`**  
  - Beschreibung: Listet Medien-Dateien (Video/Audio/Bilder) auf.  
  - Parameter: `audio`, `photo`, `dirid`, `thumbs`, `m3u`, `recursive`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/mediafiles.html?video=1&dirid=1&recursive=1"
    ```

- **`/api/recordings.html`**  
  - Beschreibung: Listet Aufnahmen auf.  
  - Parameter: `utf8`, `nofilename`, `images`, `id`, `eventid`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/recordings.html?images=1"
    ```

- **`/api/recdelete.html`**  
  - Beschreibung: Löscht Aufnahmen.  
  - Parameter: `recid` oder `recfile`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/recdelete.html?recid=123&delfile=1"
    ```

- **`/api/recedit.html`**
  - Beschreibung: Bearbeitet die Metadaten einer Aufnahme (z.B. Startzeit, Dauer).
  - Parameter: `id`, `start`/`isostart`, `duration`/`isoduration`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/recedit.html?id=123&isostart=20250724T201500"
    ```

- **`/api/recordcount.html`**
  - Beschreibung: Gibt die Anzahl der Aufnahmen zurück.
  - Parameter: `withtimeshift`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/recordcount.html?withtimeshift=1"
    ```

- **`/api/recordstats.html`**  
  - Beschreibung: Statistik zu laufenden Aufnahmen (Datenrate, Dateigröße, etc.).
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/recordstats.html?id=456"
    ```

---

### **5. EPG (Electronic Program Guide)**
- **`/api/epg.html`**  
  - Beschreibung: Liefert EPG-Daten.  
  - Parameter: `channel`, `start`/`end`, `search`, `utc`, `xmltv`, `xgrab`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/epg.html?channel=562954315180093&search=News"
    ```

- **`/api/epgclear.html`**  
  - Beschreibung: Löscht EPG-Daten.  
  - Parameter: `source` (DVB/MHW/externe Quelle).
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/epgclear.html?source=4"
    ```

- **`/cgi-bin/EPGimport`** (HTTP POST)  
  - Beschreibung: Importiert EPG-Daten im XML-Format.
  - **Beispielaufruf (curl):**
    ```bash
    curl -X POST --header "Content-Type: text/xml" --data-binary "@epgdata.xml" "http://localhost:8000/cgi-bin/EPGimport"
    ```

---

### **6. Timer**
- **`/api/timerlist.html`**  
  - Beschreibung: Listet Timer auf.  
  - Parameter: `utf8`, `id`, `reconly`, `enabledonly`, `withtimeshift`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/timerlist.html?reconly=1"
    ```

- **`/api/timeradd.html`**  
  - Beschreibung: Erstellt einen neuen Timer.  
  - Parameter: `ch`, `dor`/`isodate`, `start`/`isostart`, `title`, `days`, `action`, `timeshift`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/timeradd.html?ch=562954315180093&isodate=2025-07-25&isostart=20:15&isostop=22:00&title=My%20New%20Timer&enable=1"
    ```

- **`/api/timeredit.html`**  
  - Beschreibung: Bearbeitet einen Timer.  
  - Parameter: Wie `timeradd.html`, plus `id`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/timeredit.html?id=123&title=My%20Edited%20Timer"
    ```

- **`/api/timerdelete.html`**  
  - Beschreibung: Löscht Timer.  
  - Parameter: `id` (Timer-ID oder Liste), `delrecfile`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/timerdelete.html?id=123,124"
    ```

- **`/api/timerrestart.html`**  
  - Beschreibung: Stoppt und startet eine Aufnahme neu.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/timerrestart.html?id=123"
    ```

---

### **7. Streaming**
- **`/channels.m3u`**, **`/rtspchannels.m3u`**  
  - Beschreibung: M3U-Playlists für Live-Streams.  
  - Parameter: `fav`, `tv`, `radio`, `tags`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/channels.m3u?fav=1&tags=58"
    ```

- **`/transcodedchannels.m3u`**
  - Beschreibung: M3U-Playlist für transkodierte Streams.
  - Parameter: `tvpreset`, `rpreset`, `fav`, `favonly`, `hls`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/transcodedchannels.m3u?tvpreset=1&hls=1&favonly=1"
    ```

- **`/api/starthls.html`**, **`/master.m3u8`**  
  - Beschreibung: Startet HLS-Streaming.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/starthls.html?chid=YOUR_CHANNEL_ID"
    ```

- **`/tv.html`**  
  - Beschreibung: WebM/TS/Flash-Streaming.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/tv.html?chid=YOUR_CHANNEL_ID"
    ```

- **`/api/startts.html`**, **`/api/stopts.html`**  
  - Beschreibung: Steuert permanente TS-Streams.
  - **Beispielaufruf (curl):**
    ```bash
    # Start
    curl "http://localhost:8000/api/startts.html?streamid=myStream&chid=YOUR_CHANNEL_ID"
    # Stop
    curl "http://localhost:8000/api/stopts.html?streamid=myStream"
    ```

---

### **8. Systemsteuerung**
- **`/api/tasks.html`**  
  - Beschreibung: Startet Systemaufgaben (EPG-Update, Standby, etc.).  
  - Parameter: `task` (z.B. `EPGStart`, `Shutdown`), `action=cancel`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/tasks.html?task=EPGStart"
    ```

- **`/api/dvbcommand.html`**  
  - Beschreibung: Steuert DVBViewer-Clients.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/dvbcommand.html?target=PC-NAME&cmd=..."
    ```

---

### **9. Spezialisierte Endpunkte**

#### **EPG und Suche**
- **`/api/searchlist.html`**  
  - Beschreibung: Listet EPG-Suchvorgaben auf.  
  - Parameter: `content`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/searchlist.html?content=3"
    ```

- **`/api/searchadd.html`**, **`/api/searchedit.html`**, **`/api/searchdelete.html`**  
  - Beschreibung: Fügt hinzu, bearbeitet oder löscht EPG-Suchvorgaben.  
  - Parameter: `SearchPhrase`, `Name`, `AutoRecording`, etc.
  - **Beispielaufruf (curl):**
    ```bash
    # Hinzufügen
    curl "http://localhost:8000/api/searchadd.html?Name=MySearch&SearchPhrase=News&AutoRecording=1"
    # Löschen
    curl "http://localhost:8000/api/searchdelete.html?id=1"
    ```

- **`/api/getepgdat.html`**  
  - Beschreibung: Liefert EPG-Daten im binären Format.
  - **Beispielaufruf (curl):**
    ```bash
    curl http://localhost:8000/api/getepgdat.html -o epg.dat
    ```

#### **Medien und Aufnahmen (Spezialisiert)**
- **`/api/sideload.html`**  
  - Beschreibung: Lädt Dateien aus Medien- oder Aufnahmeverzeichnissen herunter.  
  - Parameter: `video`/`audio`/`photo`/`rec`, `dirid`, `file`, `fileid`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/sideload.html?rec=1&fileid=10&file=.log"
    ```

- **`/api/sql.html`**  
  - Beschreibung: Führt SQLite-Abfragen auf Datenbanken aus (nur lesend).  
  - Parameter: `video`/`audio`/`photo`/`rec`, `query`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/sql.html?rec=1&query=SELECT%20*%20FROM%20recordings"
    ```

#### **Streaming (Spezialisiert)**
- **`/api/rtp/`**  
  - Beschreibung: Konfiguriert permanente UDP/RTP-Streams (RTSP).  
  - Parameter: `ip`, `port`, `nic`, `ttl`, `rtcp`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/api/rtp/?ip=239.0.0.1&port=5018&chid=YOUR_CHANNEL_ID"
    ```

- **`/flashstream/stream.ts`**  
  - Beschreibung: Zugriff auf permanente TS-Streams (via `streamid`).
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/flashstream/stream.ts?streamid=myStream"
    ```

#### **UPnP und Sat>IP**
- **`/upnp/channelstream/`**  
  - Beschreibung: Streamt Kanäle via UPnP mit Sat>IP-Parametern (`tnr`).  
  - Parameter: `tnr`.
  - **Beispielaufruf (curl):**
    ```bash
    curl "http://localhost:8000/upnp/channelstream/?tnr=..."
    ```

- **`/logos/`**  
  - Beschreibung: Liefert Kanal-Logos.
  - **Beispielaufruf (curl):**
    ```bash
    # Nach Channel-ID
    curl "http://localhost:8000/logos/?chid=YOUR_CHANNEL_ID"
    # Nach Dateiname
    curl "http://localhost:8000/logos/zdfhd.png"
    ```

---

### **10. Deprecated Endpunkte**
- **`/api/status.html`** (Ersetzt durch: `/api/status2.html`)
- **`/tasks.html?task`** (Ersetzt durch: `/api/tasks.html`)
- **`/index.html?epg_clear=true`** (Ersetzt durch: `/api/epgclear.html`)
- **`/api/getchannelsdat.html`** (Ersetzt durch: `/api/getconfigfile.html` oder `/api/getchannelsxml.html`)
- **`/api/getdiseqcxml.html`** (Ersetzt durch: `/api/getconfigfile.html?file=DiSEqC.xml`)
- **`/api/getfavourites.html`** (Ersetez durch: `/api/getconfigfile.html` oder `/api/getchannelsxml.html`)
- **`/api/shutdown.html`** (Ersetzt durch: `/api/tasks.html?action=cancel`)