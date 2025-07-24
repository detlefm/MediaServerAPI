# Projektkontext: MediaServer API Proxy

Dieses Projekt implementiert einen Python FastAPI-Server, der als Proxy für die MediaServer API fungiert. Die Hauptaufgabe besteht darin, die in der Dokumentation beschriebenen API-Endpunkte zu implementieren und Anfragen an den eigentlichen MediaServer unter `http://winserver-2:8089` weiterzuleiten.
Zum Testen und zur Dokumentation soll außerdem die unter `works/Endpoints.md` beschriebene API erweitert werden.

## API-Dokumentation

Die Grundlage für alle Entwicklungsaufgaben sind die folgenden Dokumente, die die MediaServer API beschreiben:

-   `ai_source/RecordingService.md`: Enthält die Kern-API-Dokumentation.
-   `ai_source/ChangesMediaServer.txt`: Beschreibt Änderungen und Ergänzungen der API über verschiedene Versionen hinweg.
-   `ai_source/Posts_of_changes.txt`: Bietet zusätzlichen Kontext zu den API-Änderungen.

## Entwicklungsumgebung

Die Entwicklung findet in einer virtuellen Python-Umgebung (`.venv`) statt. Es wird davon ausgegangen, dass diese Umgebung bereits erstellt und im Terminal aktiviert ist, bevor Entwicklungs- oder Ausführungsbefehle ausgeführt werden.
