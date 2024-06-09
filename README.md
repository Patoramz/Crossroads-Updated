Crossroads/Being: Ein Django-basiertes Choose-Your-Own-Story-Spiel

Projektübersicht

Crossroads/Being ist ein interaktives, textbasiertes Spiel, in dem Spieler ihre eigene Geschichte erstellen und erleben können. Das Spiel generiert einzigartige Erzählungen basierend auf den Eingaben der Benutzer und ermöglicht es den Spielern, Entscheidungen zu treffen, die den Verlauf ihrer Geschichte beeinflussen. Der Slogan des Spiels, "Thursday Whenever Wherever," fasst das Ziel zusammen, immersive Erlebnisse jederzeit und überall zu bieten.

Funktionsweise
Charaktererstellung: Benutzer geben persönliche Details wie Name, Alter, Persönlichkeitseigenschaften und Hintergrundinformationen ein.
Geschichtengenerierung: Das Spiel erstellt eine Hintergrundgeschichte und ein Setting für den Charakter, maßgeschneidert auf die Eingaben des Benutzers.
Interaktive Entscheidungen: Der Spieler navigiert durch die Geschichte, indem er Entscheidungen trifft, die die Erzählung und die Charakterstatistiken beeinflussen.
Dynamisches Erzählen: Jede Entscheidung führt zu unterschiedlichen Szenarien, was jedes Durchspielen einzigartig macht.
Hauptmerkmale

Personalisierte Erzählungen: Geschichten werden basierend auf den Eingaben des Spielers generiert und machen jedes Spiel einzigartig.
Entscheidungsgetriebenes Gameplay: Spieler treffen Entscheidungen, die den Verlauf der Geschichte und die Entwicklung des Charakters beeinflussen.
Statistikverfolgung: Das Spiel verfolgt verschiedene Statistiken wie moralischer Kompass, Ruf und Fähigkeiten, die sich basierend auf den Entscheidungen der Spieler entwickeln.
Fesselnde Kontexte: Szenarien können von alltäglichen Aktivitäten bis hin zu historischen oder fantastischen Umgebungen reichen, wie z.B. Nachrichten während des Zweiten Weltkriegs oder als Maya-Krieger.
Verwendete Technologien

Backend: Python, Django
Frontend: HTML, CSS
Datenbank: Vektordatenbanken (z.B. Pinecone)
API-Integration: OpenAI GPT API zur Geschichtengenerierung
Authentifizierung: Benutzerverwaltung und Sitzungsverwaltung


Zukünftige Verbesserungen

Verbesserungen Phase 1:
Mehr Metadaten hinzufügen und Hilfsmethoden erstellen, um die Informationen über jedes Segment zu verkürzen.
Feintuning des Dion-GPT abschließen, um die aktuellen Statistiken für den Erfolg einiger Entscheidungen zu berücksichtigen.
Zwei weitere feinabgestimmte GPTs erstellen:
Ein GPT für die Anpassung der Statistiken basierend auf den Konsequenzen und dem Tempo der Geschichte.
Ein GPT für die Änderung von Standort und Zeit.
Alle sensiblen Informationen in einer Umgebungsdatei speichern.
Datenstreaming von GPT implementieren, anstatt alle Daten auf einmal zu senden.
JavaScript hinzufügen, um diese Anfragen zu bearbeiten.
Asynchrone Anfragen zur Zeitoptimierung erstellen.
Sobald alles effizient und mit minimalen Fehlern funktioniert, das Frontend basierend auf der Sigma-Vorlage entwickeln.

Verbesserungen Phase 2:
Entwicklung der gesamten Benutzeroberfläche und eines guten Frontends für die gesamte App.
Eine Funktion hinzufügen, die basierend auf den Eingaben ein Profilbild des Benutzers erstellt.
Eine Funktion hinzufügen, die ein Bild des aktuellen Spielstandorts erstellt (dalle, fireworks.ai).

Verbesserungen Phase 3:
Eine Telefonfunktion hinzufügen, um mit interessanten Personen zu chatten.
Die Website bereitstellen.
Mit dem Marketing beginnen.
