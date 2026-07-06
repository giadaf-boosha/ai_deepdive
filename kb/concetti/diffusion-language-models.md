---
name: Diffusion Language Models
aliases: [diffusion language model, text diffusion, DLM, modello di diffusione testuale, generazione diffusiva, non-autoregressive generation, masked diffusion]
categoria: architettura
created: 2026-06-12
last_updated: 2026-06-12
---

# Diffusion Language Models

## Cos'e

Un diffusion language model (DLM) genera testo applicando un processo di diffusione inversa: parte da una sequenza di token "corrotti" (rumorosi o mascherati) e li denoisa iterativamente in parallelo fino a produrre il testo finale. L'alternativa classica — l'architettura autoregressiva che genera un token alla volta, da sinistra a destra, condizionato su tutti i precedenti — e' presente in ogni LLM mainstream dal 2017 a oggi (GPT, BERT in decodifica, LLaMA, Claude, Gemini). Il DLM rompe questa assunzione: genera l'intero blocco di output simultaneamente, modificandolo iterativamente in piu' passi di denoising.

La motivazione pratica e' la velocita'. Nella decodifica autoregressiva, ogni token richiede un forward pass completo del modello. Su un transformer da 70B parametri con KV cache, generare 1.000 token richiede 1.000 forward pass sequenziali — la latenza e' inevitabilmente proporzionale alla lunghezza dell'output. Un DLM che genera 256 token in parallelo in un singolo forward pass rompe questa proporzionalita': a parita' di throughput hardware, produce output piu' lunghi in meno tempo. Su DiffusionGemma (Google, giugno 2026), il vantaggio misurato e' 4x rispetto a Gemma 4 autoregressivo sullo stesso hardware, con 1.000+ token al secondo su H100 e 700+ su RTX 5090.

Il trade-off e' la qualita'. I DLM attuali faticano sui task che richiedono ragionamento multi-step rigoroso (matematica competitiva, inferenza logica incatenata), dove la generazione autoregressiva — che forza il modello a "pensare" token per token, mantenendo uno stato interno coerente lungo l'intera sequenza — ha un vantaggio strutturale. DiffusionGemma ottiene 69,1% su AIME 2026 contro l'88,3% di Gemma 4 autoregressivo: un divario di 19 punti che riflette il limite fondamentale del paradigma parallelo sui task di ragionamento.

## Come funziona

Il processo di diffusione testuale si ispira ai modelli di diffusione per immagini (DDPM, DALL-E 3, Stable Diffusion) ma opera su sequenze discrete di token invece che su spazi continui di pixel.

**Forward process (corruzione).** Durante il training, il testo originale viene progressivamente corrotto aggiungendo rumore: in alcune varianti i token vengono sostituiti con token casuali (Gaussian-inspired noise sul vocabolario), in altre mascherati completamente (masked diffusion, ispirata a BERT). Il modello apprende a ricostruire il testo originale partendo da versioni progressivamente piu' rumorose.

**Reverse process (denoising).** A inferenza, il modello parte da una sequenza completamente rumorosa o mascherata e applica T passi di denoising, ciascuno che stima la versione meno rumorosa della sequenza. Il numero di passi T e' un iperparametro critico: T alto produce output di qualita' maggiore ma riduce il guadagno di velocita'; T basso e' piu' veloce ma introduce artefatti. In DiffusionGemma, Google usa T=20-30 come compromesso tra qualita' e velocita' per i benchmark pubblicati.

**Attention bidirezionale.** Il componente architetturale che distingue un DLM da un LLM autoregressivo e' il tipo di attention: i DLM usano attention bidirezionale (come BERT) invece di causale. Ogni token puo' "vedere" tutti gli altri token nella sequenza — sia quelli precedenti che quelli successivi — durante ogni passo di denoising. Questo e' possibile perche' nel processo diffusivo non si genera token per token: si raffina l'intera sequenza come un blocco unico. L'attention bidirezionale permette al modello di correggere errori globali nella sequenza — inconsistenze tra il token 10 e il token 200 — che l'attention causale non puo' intercettare durante la generazione.

**Self-correction.** Un vantaggio emergente dell'architettura diffusiva e' la capacita' di auto-correzione: in passi di denoising successivi, il modello puo' tornare su token gia' generati e modificarli in funzione del contesto globale che si sta rivelando. Nella generazione autoregressiva questo non e' possibile: il token generato al passo k e' fisso e condiziona tutti i passi successivi. In DiffusionGemma, Google cita questa capacita' come uno dei motivi per cui il modello e' robusto su task di instruction following dove la risposta richiede struttura globale (tabelle, JSON, formati vincolati).

**Backbone MoE.** DiffusionGemma usa come backbone l'architettura Gemma 4 26B Mixture of Experts con 3,8B parametri attivi per forward pass. Il MoE riduce il costo computazionale per token: solo una frazione degli esperti viene attivata per ciascun token, mantenendo la capacita' totale del modello (26B) senza pagare il costo computazionale pieno a ogni inferenza. La combinazione MoE + text diffusion produce un moltiplicatore di efficienza: il DLM genera in parallelo e il MoE riduce il costo per token.

## Varianti / approcci

| Variante | Meccanismo | Esempio |
|---|---|---|
| Masked diffusion | Maschera progressiva dei token, ricostruzione bidirezionale | MDT, MDLM, DiffusionGemma |
| Gaussian diffusion su spazio continuo | Embedding continui con rumore gaussiano | CDCD, DiffuSeq |
| Score-based generative models | Stima del gradiente del log della densita' | SSD-LM |
| Discrete diffusion (absorbing) | Token assorbiti da un simbolo speciale, ricostruiti | D3PM |
| Retrieval-augmented diffusion | Condizionamento sulla KV cache di documenti recuperati | RAG-Diffusion (ricerca) |

La variante dominante nel 2026 e' la masked diffusion: e' la piu' compatibile con i transformer pre-addestrati esistenti (e' possibile fare fine-tuning di modelli BERT-like verso DLM con overhead limitato) e produce la migliore qualita' sui benchmark comuni. DiffusionGemma usa masked diffusion costruita sul backbone Gemma 4.

## Quando usarlo / quando no

**Usarlo quando:**
- Il workload e' latency-sensitive con output lunghi: generare 2.000 token di risposta in 2 secondi invece di 8 e' rilevante per chatbot interattivi, generazione di codice boilerplate, sintesi documentale.
- Il hardware e' locale o a bassa disponibilita': il profilo di throughput dei DLM (alto parallelismo su GPU consumer) e' piu' favorevole per deployment self-hosted su RTX 5090 o H100 rispetto alla decodifica autoregressiva.
- Il task ha struttura globale vincolata: JSON, tabelle, formati con dipendenze non locali. La self-correction bidirezionale aiuta a rispettare il formato senza post-processing.
- L'output e' "flat" (testo descrittivo, riassunti, traduzioni): qui il gap di qualita' rispetto all'autoregressivo e' trascurabile.

**Non usarlo quando:**
- Il task richiede ragionamento matematico o logico multi-step: su AIME, GPQA, benchmark di ragionamento simbolico, i DLM attuali perdono 15-20 punti rispetto ai modelli autoregressivi equivalenti. Il gap e' strutturale, non solo una questione di training: la generazione parallela non supporta il "chain-of-thought" step-by-step che e' il meccanismo di successo dei reasoning model.
- La qualita' e' critica in produzione: DiffusionGemma e' classificato come sperimentale da Google. Nessun DLM di produzione e' disponibile pubblicamente al giugno 2026 da un frontier lab; il paradigma e' in fase di ricerca applicata.
- Il token budget e' fisso e piccolo: il vantaggio di velocita' dei DLM emerge su sequenze lunghe (256+ token). Per output corti (< 50 token), la generazione autoregressiva e' comparabile in latenza.

## Esempi pratici

**Deployment locale ad alta velocita'.** Un developer che usa DiffusionGemma via GGUF su un M4 Ultra o su una RTX 5090 ottiene throughput paragonabile a un server cloud per output testuali non-reasoning. Il caso d'uso tipico e' un tool di assistenza alla scrittura, un generatore di test, o un agent che produce report strutturati (JSON, markdown), dove la risposta deve arrivare in meno di 3 secondi su hardware locale.

**Real-time generation in applicazioni consumer.** La velocita' dei DLM li rende candidati per applicazioni dove la generazione deve tenere il passo con l'utente: completamento di testo in tempo reale mentre si scrive, generazione di sottotitoli in diretta, assistente vocale con output testuale immediato. NVIDIA accelera DiffusionGemma specificatamente per questi scenari (NIM, deployment su laptop con RTX).

**Batching ad alta concorrenza.** Un server di inference che deve servire 500 richieste parallele puo' beneficiare del throughput superiore dei DLM rispetto all'autoregressivo: invece di allocare KV cache per 500 sequenze autoregressiva distinte, un DLM genera 256 token in un singolo forward pass con footprint memoria comparabile. Il vantaggio dipende dal profilo del workload: DLM e' piu' efficiente se le richieste sono brevi e frecuenti, autoregressivo se le richieste sono lunghe e il context e' dominante.

## Letture

- Austin et al., "Structured Denoising Diffusion Models in Discrete State-Spaces" (D3PM), NeurIPS 2021. https://arxiv.org/abs/2107.03006
- Gong et al., "DiffuSeq: Sequence to Sequence Text Generation with Diffusion Models", ICLR 2023. https://arxiv.org/abs/2210.08933
- Sahoo et al., "Simple and Effective Masked Diffusion Language Models" (MDLM), 2024. https://arxiv.org/abs/2406.07524
- Google DeepMind, "DiffusionGemma: The Developer Guide", 2026. https://developers.googleblog.com/diffusiongemma-the-developer-guide/
- Google AI for Developers, "DiffusionGemma model card", 2026. https://ai.google.dev/gemma/docs/diffusiongemma/model_card

## Aggiornamenti

### 2026-06-12

Google DeepMind rilascia DiffusionGemma il 10 giugno 2026: primo DLM open da un lab frontier, basato su backbone Gemma 4 26B MoE (3,8B attivi), architettura masked diffusion con attention bidirezionale, 4x piu' veloce di Gemma 4 autoregressivo (1.000 tok/s H100, 700+ RTX 5090), contesto 256K, 140+ lingue, licenza Apache 2.0. La comunita' ha rilasciato quantizzazioni NVFP4 (NVIDIA) e GGUF (Unsloth) nelle prime 24 ore. Il trade-off di qualita' e' esplicito: AIME 2026 69,1% vs 88,3% autoregressivo. Google classifica il modello come sperimentale. Primo DLM con adozione concreta su piattaforme di serving standard (HuggingFace, NVIDIA NIM). 13+ fonti indipendenti. [Digest 2026-06-12](../../digest/2026/06/12.md)
