# Prompt
Schreibe eine PowerShell Funktion die bei einem erfolgreichem Web API Call zusätzlich zu dem Text Content noch die Response Header zurückgibt


# DeepSeek Answer


Hier ist eine PowerShell-Funktion, die einen Web-API-Aufruf durchführt und bei Erfolg sowohl den Inhalt (Content) als auch die Response-Header zurückgibt:

```powershell
function Invoke-WebApiWithHeaders {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Uri,
        
        [Parameter(Mandatory=$false)]
        [Microsoft.PowerShell.Commands.WebRequestMethod]$Method = 'Get',
        
        [Parameter(Mandatory=$false)]
        [object]$Body,
        
        [Parameter(Mandatory=$false)]
        [System.Collections.IDictionary]$Headers
    )

    try {
        # Führe den Web-Request aus
        $response = Invoke-WebRequest -Uri $Uri -Method $Method -Body $Body -Headers $Headers
        
        # Erstelle ein benutzerdefiniertes Objekt mit Inhalt und Headern
        $result = [PSCustomObject]@{
            Content = $response.Content
            Headers = $response.Headers
            StatusCode = $response.StatusCode
            StatusDescription = $response.StatusDescription
        }
        
        return $result
    }
    catch {
        # Wenn der Request fehlschlägt, aber eine Antwort erhalten wurde (z.B. 404)
        if ($_.Exception.Response) {
            $errorResponse = $_.Exception.Response
            
            $result = [PSCustomObject]@{
                Content = $null
                Headers = $errorResponse.Headers
                StatusCode = $errorResponse.StatusCode
                StatusDescription = $errorResponse.StatusDescription
                ErrorMessage = $_.Exception.Message
            }
            
            return $result
        }
        else {
            # Bei anderen Fehlern (z.B. keine Verbindung)
            throw $_
        }
    }
}
```

### Verwendung der Funktion:

```powershell
# Beispielaufruf
$apiResponse = Invoke-WebApiWithHeaders -Uri "https://api.example.com/data" -Method Get

# Ausgabe der Ergebnisse
Write-Host "Status Code: $($apiResponse.StatusCode)"
Write-Host "Content: $($apiResponse.Content)"
Write-Host "Headers:"
$apiResponse.Headers.GetEnumerator() | ForEach-Object {
    Write-Host "$($_.Key): $($_.Value)"
}
```

### Features:
1. Gibt ein Objekt mit `Content`, `Headers`, `StatusCode` und `StatusDescription` zurück
2. Behandelt erfolgreiche und fehlgeschlagene Requests (mit HTTP-Fehlercodes)
3. Unterstützt verschiedene HTTP-Methoden (GET, POST, PUT, etc.)
4. Akzeptiert optionale Request-Bodies und Header
5. Fängt Fehler ab und gibt strukturierte Fehlerinformationen zurück

### Erweiterungsmöglichkeiten:
- Hinzufügen von Authentifizierungsparametern
- Unterstützung für verschiedene Content-Typen (JSON, XML, etc.)
- Timeout-Einstellungen
- Cookie-Handling


# Prompt
Mach mir daraus ein Modul das ich von der Kommandozeile aufrufen kann.

# DeepSeek Answer

## Umwandlung der Funktion in ein PowerShell-Skript

Hier ist die Funktion als eigenständiges PowerShell-Skript (`Invoke-WebApiWithHeaders.ps1`):

```powershell
<#
.SYNOPSIS
    Führt einen Web-API-Request mit benutzerdefinierten Headern aus und gibt eine strukturierte Antwort zurück.

.DESCRIPTION
    Diese Funktion führt einen Web-Request durch und gibt ein Objekt mit Inhalt, Headern und Statusinformationen zurück.
    Sie behandelt auch Fehlerantworten der API und gibt diese strukturiert zurück.

.PARAMETER Uri
    Die URL der aufzurufenden Web-API (erforderlich).

.PARAMETER Method
    Die HTTP-Methode (GET, POST, PUT, DELETE etc.). Standard ist GET.

.PARAMETER Body
    Der Request-Body (für POST/PUT etc.).

.PARAMETER Headers
    Ein Hashtable mit den gewünschten HTTP-Headern.

.EXAMPLE
    .\Invoke-WebApiWithHeaders.ps1 -Uri "https://api.example.com/data" -Method Get

.EXAMPLE
    $headers = @{ "Authorization" = "Bearer token123"; "Accept" = "application/json" }
    .\Invoke-WebApiWithHeaders.ps1 -Uri "https://api.example.com/data" -Method Post -Body $body -Headers $headers
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$Uri,
    
    [Parameter(Mandatory=$false)]
    [Microsoft.PowerShell.Commands.WebRequestMethod]$Method = 'Get',
    
    [Parameter(Mandatory=$false)]
    [object]$Body,
    
    [Parameter(Mandatory=$false)]
    [System.Collections.IDictionary]$Headers
)

try {
    # Führe den Web-Request aus
    $response = Invoke-WebRequest -Uri $Uri -Method $Method -Body $Body -Headers $Headers
    
    # Erstelle ein benutzerdefiniertes Objekt mit Inhalt und Headern
    $result = [PSCustomObject]@{
        Content = $response.Content
        Headers = $response.Headers
        StatusCode = $response.StatusCode
        StatusDescription = $response.StatusDescription
    }
    
    # Ausgabe des Ergebnisses
    $result
}
catch {
    # Wenn der Request fehlschlägt, aber eine Antwort erhalten wurde (z.B. 404)
    if ($_.Exception.Response) {
        $errorResponse = $_.Exception.Response
        
        $result = [PSCustomObject]@{
            Content = $null
            Headers = $errorResponse.Headers
            StatusCode = $errorResponse.StatusCode
            StatusDescription = $errorResponse.StatusDescription
            ErrorMessage = $_.Exception.Message
        }
        
        # Ausgabe des Fehlerergebnisses
        $result
    }
    else {
        # Bei anderen Fehlern (z.B. keine Verbindung)
        Write-Error $_.Exception.Message
        exit 1
    }
}
```

## Anwendung des Skripts

1. Speichern Sie den Code als `Invoke-WebApiWithHeaders.ps1`
2. Führen Sie es wie folgt aus:

### Einfacher GET-Request:
```powershell
.\Invoke-WebApiWithHeaders.ps1 -Uri "https://api.example.com/data"
```

### POST-Request mit Headers und Body:
```powershell
$headers = @{
    "Authorization" = "Bearer token123"
    "Content-Type" = "application/json"
}
$body = @{
    name = "Test"
    value = 123
} | ConvertTo-Json

.\Invoke-WebApiWithHeaders.ps1 -Uri "https://api.example.com/data" -Method Post -Body $body -Headers $headers
```

### Von der CMD-Eingabeaufforderung:
```cmd
powershell -File "Invoke-WebApiWithHeaders.ps1" -Uri "https://api.example.com/data"
```

## Verbesserungen gegenüber der reinen Funktion

1. **Dokumentation**: Das Skript enthält ausführliche Hilfe-Kommentare
2. **Fehlerbehandlung**: Bei schweren Fehlern wird mit `exit 1` beendet
3. **Ausgabe**: Die Ergebnisse werden direkt ausgegeben, nicht nur zurückgegeben
4. **Standalone-Fähigkeit**: Das Skript kann unabhängig von einer bestimmten PowerShell-Sitzung ausgeführt werden