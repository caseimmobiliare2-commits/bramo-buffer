# CH.RENTALS → Buffer → Google Business Profile

Questo progetto programma l'invio dei post approvati in `posts.json` alla **coda di Buffer**. Non genera nuovi post con IA: per farlo serve aggiungere successivamente una fonte di contenuti e un servizio AI. Il Mac può rimanere spento.

## Setup

1. Crea un repository **privato** su github.com e carica tutti i file conservando la cartella `.github/workflows`.
2. In GitHub apri **Settings → Secrets and variables → Actions**.
3. In **Secrets** → **New repository secret** crea `BUFFER_API_KEY`, incollando la chiave personale Buffer. **Non inserirla mai nei file o nei messaggi.**
4. In **Variables** → **New repository variable** crea `BUFFER_CHANNEL_ID` con l'ID del canale Google Business collegato in Buffer (non è il nome della scheda).
5. Per ottenere l'ID del canale, usa l'API Explorer di Buffer: esegui `query { account { organizations { id } } }`, poi `query { channels(input: { organizationId: "INSERISCI_ID" }) { id name service } }` e scegli il canale Google Business. Guida ufficiale: https://developers.buffer.com/guides/your-first-post.html
6. Controlla e modifica i tre testi e le date in `posts.json` prima di attivare il workflow. Le date sono nel formato `AAAA-MM-GG`, fuso Europe/Zurich.
7. In **Actions** puoi usare **Run workflow** per testare. IMPORTANTE: un'esecuzione manuale in un giorno con un post previsto lo aggiunge realmente alla coda. Ripetere il workflow lo duplica.

## Calendario

Il job parte di norma ogni giorno verso le **08:15 UTC** (09:15 orario invernale, 10:15 estivo svizzero). I workflow GitHub Actions programmati possono subire ritardi o occasionali omissioni. Il programma non crea nulla nei giorni senza testi approvati, quindi **dopo le tre date di esempio smette di inviare contenuti**.

Il post viene **aggiunto alla coda Buffer**, non pubblicato immediatamente; imposta gli orari della coda su Buffer. Nel piano Free i post in attesa sono limitati.

## Note di sicurezza

La chiave API rimane nei GitHub Actions Secrets, non nei file. Non abilitare contributi di terzi al repository. Il programma NON impedisce duplicati in caso di riavvii nello stesso giorno. La procedura non garantisce pubblicazioni se Buffer, l'API, o il workflow GitHub non sono disponibili.

API Buffer: https://developers.buffer.com/guides/posts-and-scheduling.html
