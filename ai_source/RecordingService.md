```markdown
# Recording Service web API

Version 1.33.1



All functions should be working with Recording Service 1.33.1 or later. If you find a problem, please report it in the Forum.

## HTTP-Requests

All requests are done to the main web server of the Recording Service. Most likely you have to do an authentication and you need the IP and web server port.

The answers from the Recording Service are XML files unless described otherwise.

All HTTP-requests use the base path `api`. Format:
```
http://[user]:[password]@[IP]:[port]/api/
```

**Reserved characters in the user and password part must use URL encoding.**  
[Wikipedia Percent-encoding](https://en.wikipedia.org/wiki/Percent-encoding#Percent-encoding_reserved_characters)

## User

There are two user accounts in the Recording Service:
- Normal user with full access
- Limited guest user (read-only access)

Use the [status2](#status2) and the rights value to determine which access you have.

## Status informations

### Version

Get the version of the service:

**Request** (HTTP GET):
```
/api/version.html
```

**Response**:
```xml
<version iver="18939904">DVBViewer Recording Service 1.33.0.0 (beta) (PC-NAME)</version>
```

- `iver`: MajorVersion × 2²⁴ + MinorVersion × 2¹⁶ + Revision × 2⁸ + Build
- Version number and PC NetBIOS name are included

### Status2

Get the status of the service:

**Request** (HTTP GET):
```
/api/status2.html
```

**Response** (XML with status information):
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
</status>
```

Key elements:
- `timercount`: Number of active timers
- `reccount`: Number of ongoing recordings
- `nexttimer`: Time in seconds until next timer starts (-1 = none)
- `rights`: `full` (unlimited access) or `read` (read-only)
- `recfolders`: Available recording folders with size and free space

## Configuration files - settings

### getconfigfile

Download files from the configuration folder:

**Request** (HTTP GET):
```
/api/getconfigfile.html?file=[path relative to configuration folder]
```

Example (get service.xml):
```
http://[user:password@]IP[:port]/api/getconfigfile.html?file=config%5Cservice.xml
```

- Use `*` as wildcard to list matching files
- Files containing "userdata" in their name are excluded

### setting

Access service.xml settings:

**Request** (HTTP GET):
```
/api/setting.html?sec=[section]&id=[identifier]&def=[def]
```

Example (get streaming port):
```
http://[user:password@]IP[:port]/api/setting.html?sec=WebGeneral&id=StreamPort&def=7522
```

## Channel/Favourite list

### getchannelsxml

Get XML channel list:

**Request** (HTTP GET):
```
/api/getchannelsxml.html[?logo=1][&rtsp=1][&upnp=1][&subchannels=1]
```

Parameters:
- `rootsonly=1`: Only root nodes
- `group=[Name]`: Filter by category
- `id=[ChannelID]`: Get specific channel
- `logo=1`: Include logo URLs
- `rtsp=1`: Include RTSP URLs
- `upnp=1`: Include UPnP URLs
- `subchannels=1`: Include audio subchannels

## Mediafiles

### mediafiles

List files in Media Libraries:

**Request** (HTTP GET):
```
/api/mediafiles.html[?audio=1][?photo=1][&dirid={directory ID}][&thumbs=1]
```

Parameters:
- `audio=1`: List music files
- `photo=1`: List image files
- `dirid`: List files in specific directory
- `thumbs=1`: Include thumbnail URLs

## Streaming

**Requests** (HTTP GET):
```
/channels.m3u
/rtspchannels.m3u
```

### HLS

**Requests** (HTTP GET):
```
/api/starthls.html?
/master.m3u8?
```

### WebM/TS/Flash

**Request** (HTTP GET):
```
/tv.html?
```

## Recordings

### recordings

Get recordings list:

**Request** (HTTP GET):
```
/api/recordings.html[?utf8=]
```

Parameters:
- `utf8=1`: UTF-8 encoded response
- `nofilename=1`: Exclude filenames
- `images=1`: Include thumbnails
- `id=[recid]`: Get specific recording

### recdelete

Delete a recording:

**Request** (HTTP GET):
```
/api/recdelete.html?recid=id&delfile=1
```

Returns "423 Locked" if recording is currently running.

## EPG

### EPG

Get EPG data:

**Request** (HTTP GET):
```
/api/epg.html?lvl=2[&channel={epgchannelID}][&start={floatDateTime}][&end={floatDateTime}][&search={term}&options={options}]
```

Parameters:
- `channel`: Filter by channel EPG ID
- `start/end`: Time range
- `search`: Search term
- `options`: Search options (T=title, S=subtitle, D=description)

### Clear EPG

Clear EPG data:

**Request** (HTTP GET):
```
/api/epgclear.html?source=[Sources]
```

### EPGimport

Add EPG data:

**Request** (HTTP POST):
```
http://[user:password@]IP[:port]/cgi-bin/EPGimport
```

Post valid EPG XML (same format as epg.html response).

## Timer

### Timer list

Get timer list:

**Request** (HTTP GET):
```
/api/timerlist.html[?utf8=2]
```

### Add a timer

Add new timer:

**Request** (HTTP GET):
```
/api/timeradd.html
```

Parameters:
- `ch`: Channel ID (32-bit or 64-bit)
- `dor`: Date (mandatory)
- `enable`: 0/1 (mandatory)
- `start/stop`: Start/end times (mandatory)
- `title`: Timer name
- `days`: For repeating timers (7-char string)
- `action`: 0=Record, 1=Tune
- `prio`: Priority (0-100)

### Edit a timer

Edit existing timer:

**Request** (HTTP GET):
```
/api/timeredit.html
```

Same parameters as adding, plus:
- `id`: TimerID (mandatory)

### Delete a timer

Delete timer:

**Request** (HTTP GET):
```
/api/timerdelete.html?id=xxxx[&delrecfile=x]
```

## control

### Recording Service tasks

Start a task:

**Request** (HTTP GET):
```
/api/tasks.html?task=[task name]
```

Example tasks:
- `EPGStart`: Start EPG Scan
- `Hibernate`: Hibernate
- `Standby`: Standby
- `Shutdown`: Shutdown
- `AutoTimer`: Run AutoTimer

### control DVBViewer clients

Get client list:

**Request** (HTTP GET):
```
/api/dvbcommand.html
```

Send command to client:

**Request** (HTTP GET):
```
/api/dvbcommand.html?target={pc name}&cmd={DVBViewer command}
```

## Deprecated functions

- `/api/status.html` → Use status2.html
- `/tasks.html?task` → Use /api/tasks.html
- `/index.html?epg_clear=true` → Use /api/epgclear.html
- `/api/getchannelsdat.html` → Use getconfigfile.html or getchannelsxml.html
- `/api/getdiseqcxml.html` → Use getconfigfile.html?file=DiSEqC.xml
- `/api/getfavourites.html` → Use getconfigfile.html or getchannelsxml.html
```