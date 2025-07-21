# Media Server (formerly Recording Service) API Documentation  
Version 3.3.1 – July 2025  
*Consolidated from all change logs and original RecordingService.md*  

All functions are guaranteed to work with Media Server 3.3.1 or later.  
For problems, please post in the official Forum.

---

## 1. General Information

### Base URL
```
http://[user]:[password]@[IP]:[port]/api/
```
- Reserved characters in `user`/`password` must be URL-encoded ([Wikipedia Percent-encoding](https://en.wikipedia.org/wiki/Percent-encoding#Percent-encoding_reserved_characters))  
- All XML responses are UTF-8 unless a different encoding is forced by the client.  
- Two user accounts exist:
  - Normal user (full access)
  - Guest user (read-only) – check `<rights>` in `/api/status2.html`

---

## 2. Status Information

### 2.1 Version
**GET** `/api/version.html`

**Response** (XML):
```xml
<version iver="18939904" inst="0" ires="0">
  DVBViewer Recording Service 1.33.0.0 (beta) (PC-NAME)
</version>
```
- `iver`: Major×2²⁴ + Minor×2¹⁶ + Revision×2⁸ + Build  
- `inst`: Zero-based instance number (0-3) – introduced in 3.3.1  
- `ires`: Bit-field restrictions (Bit 0 = read-only, Bit 1 = no EPG update task, Bit 2 = no auto-timer task) – introduced in 2.1.5

---

### 2.2 Status2
**GET** `/api/status2.html`

**Response** (XML):
```xml
<status>
  <timercount>0</timercount>
  <reccount>0</reccount>
  <nexttimer>-1</nexttimer>
  <nextrec>-1</nextrec>
  <streamclientcount>0</streamclientcount>
  <rtspclientcount>0</rtspclientcount>
  <unicastclientcount>0</unicastclientcount>
  <lastuiaccess>13</lastuiaccess>
  <standbyblock>1</standbyblock>
  <tunercount>0</tunercount>
  <streamtunercount>0</streamtunercount>
  <rectunercount>0</rectunercount>
  <epgudate>0</epgudate>
  <rights>full</rights>
  <recfiles>2</recfiles>
  <recfolders>
    <folder size="1445946646528" free="15966986240">
      E:\Recorded TV
    </folder>
    <folder size="57404289024" free="3202850816">
      C:\Users\Public\Recorded TV
    </folder>
  </recfolders>
  <timezone>120</timezone>
</status>
```
- `<timezone>` added in 3.1.0 (bias in minutes)

---

## 3. Configuration Files – Settings

### 3.1 getconfigfile
**GET** `/api/getconfigfile.html?file=[relativePath]`

- Wildcard `*` allowed  
- `userdata*` files are excluded  
- From 2.1.2 the file `config\service.xml` is served from memory (unsaved changes included)

**Examples**  
curl:
```bash
curl -u user:pass "http://192.168.1.2:8089/api/getconfigfile.html?file=config%5Cservice.xml"
```
Python:
```python
import requests
url = "http://192.168.1.2:8089/api/getconfigfile.html"
params = {"file": r"config\service.xml"}
r = requests.get(url, params=params, auth=("user", "pass"))
print(r.text)
```

---

### 3.2 setting
**GET** `/api/setting.html?sec=[section]&id=[identifier]&def=[default]`

Returns plain text value of the requested key.

**Example**  
Get streaming port:
```
http://user:pass@192.168.1.2:8089/api/setting.html?sec=WebGeneral&id=StreamPort&def=7522
```

---

## 4. Channel/Favourite List

### 4.1 getchannelsxml
**GET** `/api/getchannelsxml.html`

**Query Parameters** (all optional):

| Param        | Type | Default | Meaning |
|--------------|------|---------|---------|
| rootsonly=1  | int  | 0       | Only root nodes |
| group=[Name] | str  | —       | Filter by category |
| id=[ChannelID]| int | —       | Single channel |
| logo=1       | int  | 0       | Include logo URLs |
| rtsp=1       | int  | 0       | Include RTSP URLs |
| upnp=1       | int  | 0       | Include UPnP URLs |
| subchannels=1| int  | 0       | Include audio subchannels |
| tvonly=1     | int  | 0       | Only TV (since 2.0) |
| radioonly=1  | int  | 0       | Only radio (since 2.0) |
| epgonly=1    | int  | 0       | Only channels with EPG (since 2.0) |
| fav=0/1      | int  | —       | Override “add favorites” setting |
| favonly=0/1  | int  | —       | Override “favorites only” setting |

**Changes**  
- 2.0: Added tvonly, radioonly, epgonly  
- 2.1.0: When single channel does not exist → empty `<channels/>` (was full list)  
- 2.1.0: rootsonly & groupsonly now respect tvonly/radioonly/epgonly

**Example**  
Return only TV favorites with logos:
```bash
curl -u user:pass "http://192.168.1.2:8089/api/getchannelsxml.html?tvonly=1&favonly=1&logo=1"
```

---

### 4.2 getlogoassignment
**GET** `/api/getlogoassignment.html?name=[ChannelName]&id=[EPGChannelID]`

- Returns logo filename or `-` if none  
- 404 if no logos available  
- Backslashes allowed in returned filename (relative to `\Images\Logos\`)

**Example**  
```bash
curl "http://192.168.1.2:8089/api/getlogoassignment.html?name=Das%20Erste&id=562954315180093"
```

---

## 5. Media Files

### 5.1 mediafiles / mediafiles2
**GET** `/api/mediafiles.html` or `/api/mediafiles2.html` *(mediafiles2 triggers 404 on old servers)*

**Parameters**:

| Param      | Type | Default | Meaning |
|------------|------|---------|---------|
| video=1    | int  | 1       | Video database |
| audio=1    | int  | 0       | Audio database |
| photo=1    | int  | 0       | Photo database |
| dirid=n    | int  | -1      | Directory ID |
| content=1/2/3 | int | 1    | 1=files, 2=directories, 3=both |
| recursive=1| int  | 0       | Walk sub-dirs |
| thumbs=1   | int  | 0       | Include thumbnail URLs |
| m3u=1      | int  | 0       | Return M3U playlist |

**Example**  
List all audio files recursively as M3U:
```bash
curl -u user:pass "http://192.168.1.2:8089/api/mediafiles.html?audio=1&recursive=1&m3u=1"
```

---

### 5.2 sideload
**GET** `/api/sideload.html`

**Parameters**:

| Param  | Type | Default | Meaning |
|--------|------|---------|---------|
| video/audio/photo/rec=1 | int | video=1 | Media type |
| dirid=n | int | — | Directory ID |
| fileid=n| int | — | File/recording ID (same as dirid for recordings) |
| file=[name] | str | — | UTF-8 filename or mask (`*` allowed) |
| download=1 | int | 0 | Force download header |

- From 2.1.0 supports recording directories  
- From 2.1.0 supports extension replacement via `.ext` (e.g. `file=.srt`)

**Examples**  
Download recording log:
```bash
curl -u user:pass "http://192.168.1.2:8089/api/sideload.html?rec=1&fileid=10&file=.log&download=1"
```

---

## 6. Streaming

### 6.1 M3U Playlists
**GET**  
- `/channels.m3u` (live)  
- `/transcodedchannels.m3u` (transcoded)  
- `/rtspchannels.m3u` (RTSP)

**Channel List Download Parameters** *(apply to all three URLs)*:

| Param  | Type | Default | Meaning |
|--------|------|---------|---------|
| tv=0/1 | int | user | Include TV channels |
| radio=0/1 | int | user | Include radio channels |
| fav=0/1 | int | user | Add favorites on top |
| favonly=0/1 | int | user | Only favorites |
| tags=n | int | tweak | Bit field for EXTINF tags (see 2.1.5) |
| tvpreset / rpreset | int/str | — | Transcoding preset |
| hls=0/1 | int | UA-based | Preset file selection |

**tags** bit values (add together):  
1 = category in name  
2 = group-title on change  
4 = group-title always  
8 = tvg-logo URL  
16 = tvg-id  
32 = tvg-name  
64 = tvg-chno  

**Example**  
HLS TV favorites only, second preset:
```
http://192.168.1.2:8089/transcodedchannels.m3u?tvpreset=1&hls=1&favonly=1
```

---

### 6.2 HLS
- Start: `/api/starthls.html?...`  
- Master playlist: `/master.m3u8?...`  

Parameters documented in `transcoding_params_en.txt` (not repeated here).

---

### 6.3 Permanent Transcoded TS
**Start**  
**GET** `/api/startts.html?streamid=[unique_name]&chid=[...]&...`

**Stop**  
**GET** `/api/stopts.html?streamid=[unique_name]`

Client URL:
```
/flashstream/stream.ts?streamid=[unique_name]
```
- Added in 2.0.0  
- Unlimited concurrent clients, single FFmpeg instance  
- WebM/Flash **not** supported

---

### 6.4 RTSP / Live Permanent UDP/RTP
**GET** `/rtp/?ip=[dest]&port=[p]&chid=[...]&...`

Required: `ip`, `port`  
Optional: `nic`, `ttl`, `rtcp=1` (Sat>IP multicast)  
Same URL toggles ON/OFF.  
Requires ≥50-client license (2.1.5).

---

## 7. Recordings

### 7.1 recordings
**GET** `/api/recordings.html`

**Parameters**:

| Param      | Type | Default | Meaning |
|------------|------|---------|---------|
| utf8=1     | int  | 0       | UTF-8 response |
| nofilename=1| int | 0       | Exclude filenames |
| images=1   | int  | 0       | Include thumbnails |
| id=[recid] | int  | —       | Single recording |

- From 3.0.0 each `<recording>` has `lastmodified` attribute (64-bit Windows FILETIME)  
- From 3.0.2 stopped recordings expose `RealFilename` and `RecID`

**Example**  
```bash
curl -u user:pass "http://192.168.1.2:8089/api/recordings.html?utf8=1&images=1"
```

---

### 7.2 recdelete
**GET** `/api/recdelete.html`

**Parameters** (one required):

- `recid=[id]` – single or comma-separated list (since 2.1.0)  
- `recfile=[path\filename]` – path must be UTF-8 & URL-encoded (since 3.1.1)  
- `delfile=1` – delete file + DB entry (works after stop since 3.0.2)

Returns `423 Locked` if recording active.  
Bulk delete error status refers only to last failure.

**Examples**  
Delete multiple recordings:
```bash
curl -u user:pass "http://192.168.1.2:8089/api/recdelete.html?recid=12,17,3&delfile=1"
```

Delete by filename:
```bash
curl -u user:pass "http://192.168.1.2:8089/api/recdelete.html?recfile=E%3A%5CRecorded%20TV%5CMyShow.ts&delfile=1"
```

---

### 7.3 recordstats
**GET** `/api/recordstats.html?id=[timerID]`

**Response** (XML attributes only):
```xml
<recordstats rate="8123456" size="1234567890" totalsize="1234567890"
             disksize="1445946646528" diskfree="15966986240"
             runtime="1800000" errors="0" vtotal="1234567890"
             vremoved="0" devicename="DVB-S2 TBS 6981"
             pids="3,101,2,102,4,103,15" />
```
- Added in 3.0.0  
- 404 if timer does not exist or not recording

---

## 8. EPG

### 8.1 epg
**GET** `/api/epg.html`

**Parameters**:

| Param        | Type | Default | Meaning |
|--------------|------|---------|---------|
| lvl=2        | int  | required| Detail level |
| channel / ch | list | —       | Comma-separated EPG Channel IDs |
| start / end  | float| —       | Delphi TDateTime range (local) |
| isostart / isoend | ISO | — | ISO8601 alternative (since 3.2.2) |
| utc=1        | int  | 0       | All times in UTC (since 2.0) |
| search=[term]| str  | —       | Search phrase |
| options=[TSD]| str  | —       | T=title, S=subtitle, D=description |
| eventid=[id] | int  | —       | Exact Event ID (since 2.0) |
| pdc=[hex]    | hex  | —       | PDC search (since 2.0) |
| xmltv=1      | int  | 0       | XMLTV compliant output (since 2.1.5) |
| source=n     | int  | 0       | Bit mask to exclude sources (1=DVB,2=MHW,4=External) |
| xgrab=[file] | str  | —       | INI grab file in config subdir (since 2.1.5) |

**Changes**  
- 2.0: added utc, eventid, pdc, source filtering  
- 2.1.5: added channel lists, xmltv, xgrab  
- 3.2.2: added ISO date/time alternatives

**Example**  
UTC XMLTV for two channels:
```bash
curl "http://192.168.1.2:8089/api/epg.html?channel=562954315180093,562954314656614&xmltv=1&utc=1"
```

---

### 8.2 epgclear
**GET** `/api/epgclear.html?source=[Sources]`

- `Sources` as bit mask: 1=DVB, 2=MHW, 4=External  
- Default (omit) = 7 (all)  
- Added in 2.0.0

---

### 8.3 EPGimport
**POST** `http://[user:pass@]IP:port/cgi-bin/EPGimport`

- Body: valid EPG XML (same format as epg.html response)  
- Asynchronous; monitor with `/api/epgstatus.html`

---

### 8.4 epgstatus
**GET** `/api/epgstatus.html`

**Response**:
```xml
<epgstatus>
  <epglang>en</epglang>
  <timezone>120</timezone>
  <importstate>0</importstate>
  <epgcount>45230</epgcount>
  <nextupdate>20250722013000</nextupdate>
  <updatetotalcount>0</updatetotalcount>
  <updatecount>0</updatecount>
</epgstatus>
```
- Added in 3.1.1

---

## 9. Timer Management

### 9.1 timerlist
**GET** `/api/timerlist.html`

**Parameters**:

| Param        | Type | Default | Meaning |
|--------------|------|---------|---------|
| utf8=0/1/2   | int  | 0       | 0=ANSI, 1=UTF-8, 2=UTF-8+channel name |
| id=[timerID] | int  | —       | Single timer |
| recid=[id]   | int  | —       | Timer that created recording |
| reconly=1    | int  | 0       | Timers with ongoing recordings |
| enabledonly=1| int  | 0       | Active (non-disabled) timers |
| withtimeshift=1 | int | 0 | Include timeshift timers (since 3.0.0) |

**Response additions since 3.0.0**  
- `<Title>`, `<Subheading>` (read-only, from EPG)  
- `<RealFilename>` & `<RecID>` after stop (3.0.2)  
- `Duration` attribute in `<Recordstat>`  
- `EPGID` attribute on `<Channel>` (2.1.0)  
- `timeshift="0/1"` attribute on `<Timer>` (3.0.0)

---

### 9.2 timeradd
**GET** `/api/timeradd.html`

**Parameters**:

| Param        | Type | Default | Meaning |
|--------------|------|---------|---------|
| ch           | int  | required| Channel ID (32/64-bit) |
| dor / isodate| date | required| Recording date |
| start / isostart | time | required| Start (minutes since midnight or ISO) |
| stop / isostop | time | required| Stop (…) |
| isodur / dur | int  | —       | Duration in minutes (alternative) |
| enable=0/1   | int  | required| Enable timer |
| title        | str  | —       | Timer name |
| days         | str  | —       | 7-char weekday mask |
| action=0/1   | int  | 0       | 0=Record, 1=Tune |
| prio=0-100   | int  | 50      | Priority |
| scheme       | str  | —       | File naming scheme (since 2.0) |
| encoding     | str  | —       | Character encoding for scheme/title/folder/series |
| timeshift=0/1| int  | 0       | Timeshift flag (since 3.0.0) |

**Changes**  
- 2.0: added scheme, encoding  
- 3.0.0: added timeshift  
- 3.0.0: returns 406 if channel/tuner unavailable (instead of silent drop)  
- 3.2.2: ISO date/time alternatives

**Example**  
Add daily timer in ISO format:
```bash
curl -u user:pass "http://192.168.1.2:8089/api/timeradd.html?ch=562954315180093&isodate=2025-07-21&isostart=20:15&isostop=21:45&enable=1&title=Evening%20News"
```

---

### 9.3 timeredit
**GET** `/api/timeredit.html`

Same parameters as `timeradd` plus `id=[timerID]` (mandatory).  
Changes same as timeradd.

---

### 9.4 timerdelete
**GET** `/api/timerdelete.html`

**Parameters**:

- `id=[timerID]` – single or comma-separated list (since 2.1.5)  
- `delrecfile=1` – also delete recording file if stopped (since 3.0.2)  
- Alternative date/time parameters same as timeradd (since 3.2.2)

---

### 9.5 timerrestart
**GET** `/api/timerrestart.html?id=[timerID]`

- Stops & deletes ongoing recording then restarts immediately  
- Shifts start to “now”, keeps duration (since 3.0.0)  
- No effect if not recording or weekly repetition

---

## 10. EPG Search Presets

### 10.1 searchlist
**GET** `/api/searchlist.html`

**Parameters**:

| Param      | Type | Default | Meaning |
|------------|------|---------|---------|
| content=0/1/2/3 | int | 0 | 0/1=presets only, 2=default only, 3=both (since 2.1.3) |

**Response**:
```xml
<searches ver="2">
  <search id="123" ...> ... </search>
</searches>
```
- `ver=2` indicates persistent IDs (since 2.1.3)

---

### 10.2 searchadd / searchedit / searchdelete
**GET** endpoints:

- `/api/searchadd.html`  
- `/api/searchedit.html?id=[id]&name=[name]`  
- `/api/searchdelete.html?id=[id]&name=[name]`

**Common Parameters** (URL query):

| Param        | Type | Default | Meaning |
|--------------|------|---------|---------|
| SearchPhrase | str  | —       | Required for add |
| Name         | str  | —       | Preset name |
| SearchFields | int  | 3       | Bit 0=title,1=subtitle,2=desc |
| IgnoreCase   | int  | -1      | 1=ignore case |
| UseRegEx     | int  | 0       | 1=regex |
| Days         | int  | 127     | Bit mask Mon-Sun |
| StartDate / isostartdate | date | — | ISO or dd.mm.yyyy |
| EndDate / isoenddate | date | — | — |
| StartTime / isostarttime | time | — | hh:mm or ISO |
| EndTime / isoendtime | time | — | — |
| DurationMin / Max | int | 0 | Minutes |
| Genre        | int  | -1      | Genre filter |
| Channels     | csv  | —       | EPG Channel IDs |
| AutoRecording| int  | 0       | Create auto-timers |
| recseries=1  | int  | 0       | Strip season/episode (since 2.1.3) |
| checkdup=1   | int  | 0       | Skip duplicates (since 2.1.3) |
| record=1     | int  | 0       | Create timers immediately (since 2.1.3) |
| recformat    | int  | —       | TV recording format (0/1/2) |
| recradioformat| int | —       | Radio recording format (0/1) |
| incremoved=1 | int  | 1       | Include removed recordings (since 2.1.0) |
| Series       | str  | —       | Series grouping string |
| RecordingFolder, RecNameScheme, RecFormat, Shutdown, AfterProcessAction, EPGBefore, EPGAfter, MonitorPDC, MonitorForStart, Priority … | same as timeradd |

**Changes**  
- 2.0.4: API introduced  
- 2.1.3: IDs persistent (`ver=2`), added content parameter  
- 2.1.3: added recseries, checkdup, record flags  
- 2.1.0: added incremoved, recradioformat  
- 3.2.2: ISO date/time parameters supported

---

## 11. Tasks & System Control

### 11.1 tasks
**GET** `/api/tasks.html`

| Param  | Type | Meaning |
|--------|------|---------|
| task=[name] | str | Execute task |
| action=[name] | str | Alias for task |
| all=1 | int | List all internal tasks (since 2.1.0) |
| action=cancel | str | Cancel delayed shutdown/hibernate (since 2.1.0) |

**Returned task list (XML)** when no parameters:
```xml
<tasklist>
  <group name="EPG">
    <task type="0">
      <name>Start EPG Update</name>
      <action>EPGStart</action>
    </task>
  </group>
</tasklist>
```
- `type`: 0=internal, 1=user process, 2=after-recording task

**Built-in tasks**:  
`EPGStart`, `Hibernate`, `Standby`, `Shutdown`, `AutoTimer`

---

### 11.2 dvbcommand
**GET** `/api/dvbcommand.html`

- List clients (no parameters)  
- Send command:  
  `/api/dvbcommand.html?target=[PCname]&cmd=[DVBViewer command]`

---

## 12. SQLite Read-Only Access
**GET** `/api/sql.html?[video/audio/photo/rec]=1&query=[SQLite query]`

- Added in 2.0.0  
- Read-only access to databases  
- Use `COLLATE SYSTEMNOCASE` for case-insensitive Unicode

**Example**  
Count video files:
```bash
curl -u user:pass "http://192.168.1.2:8089/api/sql.html?video=1&query=SELECT COUNT(*) FROM video"
```

---

## 13. Key-Value Store (Add-ons)
**GET** `/api/store.html`

**Actions**:

| Action   | Required Parameters | Meaning |
|----------|---------------------|---------|
| write    | sec, key, value     | Store value |
| read     | sec, key            | Retrieve value (plain text) |
| delete   | sec, key (optional) | Delete key/section |
| updatefile | — | Flush to `config\AddOnStore.xml` |

**Example**  
Write:
```bash
curl "http://192.168.1.2:8089/api/store.html?action=write&sec=myAddon&key=volume&value=75"
```

---

## 14. Subtitle Delivery
Since 2.1.0 the servers deliver SRT files matching video URLs:

Replace extension:
```
/upnp/video/388.mkv  →  /upnp/video/388.srt
```
- Prefers exact filename match, else prefix match  
- 404 if no subtitle

---

## 15. Deprecated and Obsolete API Calls

| Deprecated Call | Replacement | Notes |
|-----------------|-------------|-------|
| `/api/status.html` | `/api/status2.html` | All data moved to status2 |
| `/tasks.html?task=...` | `/api/tasks.html?task=...` | Unified endpoint |
| `/index.html?epg_clear=true` | `/api/epgclear.html?source=...` | Full source control |
| `/api/getchannelsdat.html` | `/api/getconfigfile.html` or `/api/getchannelsxml.html` | — |
| `/api/getdiseqcxml.html` | `/api/getconfigfile.html?file=DiSEqC.xml` | — |
| `/api/getfavourites.html` | `/api/getconfigfile.html` or `/api/getchannelsxml.html` | — |
| `/api/shutdown.html` | `/api/tasks.html?action=cancel` or `task=Shutdown` | Merged into tasks |


