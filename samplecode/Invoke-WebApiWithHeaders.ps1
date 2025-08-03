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