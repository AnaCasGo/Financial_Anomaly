# Synthetic Data Generation

## 1. Overview

This project uses fully synthetic data to simulate the activity of a Spanish bank.

The objective is not to reproduce the Spanish population exactly, nor to create a statistically representative sample of real bank customers. Instead, publicly available demographic and labour-market statistics are used to establish realistic assumptions for the synthetic population.

The synthetic data generation process is designed to create heterogeneous customer behaviour that can later be used to study statistical and machine learning approaches to financial anomaly detection.

The generation process follows this structure:

```text
Public Spanish Statistics
        │
        ▼
Synthetic Population Assumptions
        │
        ▼
Customer Generation
        │
        ▼
Behavioural Parameters
        │
        ▼
Historical Transactions
        │
        ▼
Customer Behaviour Profiles
        │
        ▼
Production Transactions
        │
        ▼
Anomaly Detection
```

---

# 2. Data Generation Philosophy

The dataset is designed around an important principle:

> Financial behaviour should emerge from customer characteristics and behavioural patterns rather than being generated as independent random observations.

For this reason, transactions are not generated using uniform random values.

Instead, each customer is assigned a set of latent behavioural parameters. These parameters influence transaction frequency, spending behaviour, geographical activity, merchant preferences, time-of-day patterns, device usage and other characteristics.

This allows the resulting transaction history to contain meaningful individual behavioural patterns.

For example, two customers may have very different normal behaviour:

```text
Customer A

Frequent online transactions
Moderate transaction amounts
High electronics spending
Occasional international transactions


Customer B

Mostly physical transactions
Low transaction frequency
Small transaction amounts
High grocery spending
Very limited international activity
```

An anomaly detection system can then identify transactions that deviate from the behaviour normally associated with each customer.

---

# 3. Reference Population

The simulated bank operates primarily in Spain.

The demographic assumptions are informed primarily by the Spanish National Statistics Institute (INE), using the 2025 Annual Population Census.

According to INE, Spain had 49,128,297 residents on 1 January 2025. Of these, 85.9% had Spanish nationality and 14.1% had foreign nationality. People aged over 64 represented 20.7% of the population.

These figures provide a reference point for the demographic structure of the synthetic population.

Source:

- Instituto Nacional de Estadística (INE), *Censo Anual de Población. Primeros resultados 2025*:
  https://ine.es/dyngs/Prensa/es/CensoVariables2025.html

The synthetic population is deliberately restricted to adults because the project simulates banking customers who can independently perform financial transactions.

Therefore, the resulting age distribution is not expected to exactly match the overall Spanish population.

---

# 4. Population Size

The initial synthetic population consists of:

| Parameter | Value |
|---|---:|
| Number of customers | 500 |
| Historical period | January–December 2025 |
| Production period | January 2026 |
| Number of merchants | 250 |

The number of customers is intentionally small enough to allow experimentation and development while still producing a sufficiently large transaction dataset.

The number of transactions is not fixed in advance.

Instead, transaction volume emerges from each customer's behavioural parameters.

This means that customers with different behavioural profiles can generate substantially different numbers of transactions.

---

# 5. Age Distribution

Age is generated using a probability distribution informed by the demographic structure of Spain.

The synthetic population is divided into age groups:

- 18–24
- 25–34
- 35–44
- 45–54
- 55–64
- 65–74
- 75+

The probabilities are calibrated against the overall age structure of the Spanish population and then re-normalised to account for the fact that the synthetic banking population contains adults only.

The objective is to reproduce the general characteristics of the Spanish population, particularly its relatively high proportion of older adults, rather than assuming a normal distribution centred around a single average age.

A population pyramid is also used as a visual reference for the shape of the Spanish age distribution.

Reference:

- PopulationPyramid.net, Spain 2025:
  https://www.populationpyramid.net/es/espa%C3%B1a/2025/

---

# 6. Nationality

Nationality is generated using the Spanish population structure as a reference.

The initial target distribution is approximately:

| Nationality group | Target proportion |
|---|---:|
| Spanish | ~85.9% |
| Foreign | ~14.1% |

This is based on the INE population figures for 1 January 2025.

For 500 synthetic customers, this corresponds approximately to:

- 430 Spanish customers
- 70 foreign customers

The exact number may vary depending on the random seed.

Foreign nationalities are not sampled uniformly. Their probabilities are weighted using the distribution of foreign residents reported by INE.

The main foreign nationalities represented in the synthetic population include:

- Morocco
- Colombia
- Romania
- Italy
- Venezuela
- United Kingdom
- China
- Peru
- Ukraine
- Honduras
- Argentina
- Germany
- Ecuador
- France
- Bulgaria
- Paraguay
- Pakistan
- Portugal
- Russia
- Brazil

According to INE, the three largest foreign nationalities in Spain on 1 January 2025 were Moroccan, Romanian and Colombian.

Source:

- Instituto Nacional de Estadística (INE), *Censo Anual de Población 2025*:
  https://ine.es/dyngs/Prensa/es/CensoVariables2025.html

---

# 7. Nationality and Financial Behaviour

Nationality is treated as a demographic characteristic and **not as a fraud indicator**.

The anomaly detection system must not assign higher risk simply because a customer has a particular nationality.

However, nationality may influence the probability of certain legitimate behaviours.

For example, some customers may have a higher probability of:

- International transfers
- Transactions in other countries
- Travel-related transactions
- Transactions involving their country of nationality

These relationships are probabilistic rather than deterministic.

For example:

```text
Foreign nationality
        ↓
Slightly higher probability of international activity
```

This distinction is important when evaluating potential bias in fraud detection systems.

---

# 8. Employment Status

Employment status is included to create a more realistic synthetic customer population.

The following categories are considered:

- Employed
- Self-employed
- Unemployed
- Student
- Retired
- Other / inactive

Employment status is not assigned independently of age.

For example:

- Younger customers have a higher probability of being students.
- Working-age customers are more likely to be employed or self-employed.
- Older customers are increasingly likely to be retired.
- Unemployment is possible among working-age customers.

The objective is to create internally consistent customer profiles rather than independently sampling every variable.

---

# 9. Occupation

Occupational categories are informed primarily by Spanish official statistics from INE and labour-market information published by SEPE.

The 2025 INE Census provides detailed information on occupations among employed residents. Among the most common occupations were:

- Education professionals
- Retail workers
- Restaurant workers
- Healthcare professionals
- Drivers
- Cleaning workers
- Administrative workers
- Construction workers
- Sales representatives
- Care workers
- Security workers
- Science, mathematics and engineering professionals
- Business and management professionals
- Personal service workers
- Agricultural workers
- Accounting and financial support workers
- Manufacturing workers
- Shop owners

The occupational structure of the synthetic population is therefore designed to reflect the broad structure of employment in Spain rather than using an arbitrary list of equally probable professions.

Source:

- Instituto Nacional de Estadística (INE), *Censo Anual de Población 2025*:
  https://ine.es/dyngs/Prensa/es/CensoVariables2025.html

Additional labour-market context is informed by:

- Servicio Público de Empleo Estatal (SEPE), Spanish labour-market statistics:
  https://www.sepe.es/

- Cámara de Comercio de Madrid, *Profesiones más demandadas en España en 2025*:
  https://cursos-formacion.camaramadrid.es/blog/profesiones-mas-demandadas-espana-2025/

Additional secondary context:

- Ibercaja, *Profesiones más demandadas en España*:
  https://www.ibercaja.es/particulares/blog/consejos-utiles/profesiones-mas-demandadas-en-espana/

Official statistics are prioritised over secondary sources when defining the actual distributions.

---

# 10. Customer Attributes

The `customers` table contains primarily static or slowly changing customer characteristics.

Initial fields:

| Column | Description |
|---|---|
| `customer_id` | Unique customer identifier |
| `date_of_birth` | Customer date of birth |
| `nationality` | Customer nationality |
| `country_of_residence` | Country of residence |
| `occupation` | Main occupation |
| `employment_status` | Current employment status |
| `customer_since` | Date on which the customer joined the bank |

Behavioural metrics such as average transaction amount, preferred country or usual transaction time are intentionally **not stored in the customer table**.

These values will instead be calculated from historical transactions.

This separation allows the project to distinguish between:

1. Customer attributes
2. Observed financial behaviour
3. Derived behavioural features

---

# 11. Latent Behavioural Parameters

Each customer is assigned behavioural parameters used internally by the synthetic data generator.

These parameters are not necessarily stored directly in the final `customers` table.

Examples include:

- Expected transactions per month
- Typical transaction amount
- Transaction amount variability
- Online transaction probability
- International transaction probability
- Night-time transaction probability
- Weekend transaction probability
- Number of devices used
- Merchant category preferences
- Geographic mobility

These parameters are influenced by customer characteristics but also contain individual-level randomness.

Therefore, customers with similar demographic characteristics can still exhibit substantially different financial behaviour.

---

# 12. Merchant Population

The synthetic bank interacts with a population of approximately 250 merchants.

The `merchants` table contains:

| Column | Description |
|---|---|
| `merchant_id` | Unique merchant identifier |
| `merchant_category` | Merchant category |
| `country` | Merchant country |
| `city` | Merchant city |

Merchant categories include:

- Grocery
- Restaurants
- Transport
- Travel
- Entertainment
- Electronics
- Clothing
- Healthcare
- Utilities
- Education
- Hotels
- Jewellery
- Luxury Goods
- Online Services

Merchant categories are not expected to have equal transaction volumes.

For example, grocery and restaurant transactions should be substantially more frequent than jewellery or luxury goods transactions.

---

# 13. Transaction Generation

The `transactions` table represents the main fact table of the project.

Initial fields include:

| Column | Description |
|---|---|
| `transaction_id` | Unique transaction identifier |
| `customer_id` | Customer performing the transaction |
| `timestamp` | Transaction date and time |
| `amount` | Transaction amount |
| `currency` | Transaction currency |
| `merchant_id` | Merchant involved |
| `country` | Transaction country |
| `city` | Transaction city |
| `device_id` | Device used |
| `payment_method` | Payment method |
| `is_online` | Whether the transaction was online |
| `transaction_type` | Type of financial transaction |

Possible transaction types include:

- Card payment
- Online payment
- Cash withdrawal
- Bank transfer

---

# 14. Transaction Amount Distribution

Transaction amounts will not be generated using a uniform distribution.

Real-world transaction amounts are expected to be right-skewed, with many relatively small transactions and fewer high-value transactions.

The generator will therefore use a skewed probability distribution, such as a log-normal distribution, as a starting point.

The parameters of the distribution will vary between customers to reflect differences in spending behaviour.

The objective is to create a distribution where:

```text
Many small transactions
        ↓
Fewer medium transactions
        ↓
Few high-value transactions
```

This also provides a natural statistical basis for later anomaly detection using percentiles, z-scores, robust statistics and machine learning.

---

# 15. Historical Period

The historical period covers:

**1 January 2025 – 31 December 2025**

This period is used to establish the behavioural baseline for each customer.

Importantly, the historical dataset is **not assumed to be perfectly clean**.

Real financial datasets can contain unusual transactions, legitimate outliers and potentially fraudulent activity that has not been identified.

Therefore, a small controlled proportion of anomalous transactions will be introduced into the historical data.

The anomaly detection models will not receive the anomaly labels.

---

# 16. Historical Anomalies

A small proportion of historical transactions will contain anomalous behaviour.

Potential anomaly types include:

- Unusually high transaction amount
- Unusual geographic location
- Unusual transaction time
- New device
- High transaction velocity
- New merchant category
- Unusual combination of multiple behavioural signals

Some unusual transactions will represent potential fraudulent behaviour, while others will represent legitimate but unusual customer behaviour.

This distinction is important because anomaly detection identifies unusual behaviour, not fraud with certainty.

---

# 17. Production Period

After the historical period, the system enters a simulated production environment.

Production data covers:

**1 January 2026 – 31 January 2026**

The anomaly detection system uses behavioural patterns learned from the historical period to evaluate new transactions.

The production period contains:

- Normal transactions
- Previously observed types of anomalies
- New anomalous combinations
- Legitimate unusual behaviour

This allows the system to be evaluated on out-of-sample data.

---

# 18. Ground Truth

Because the data is synthetic, the generation process has access to the true state of every generated transaction.

A separate ground-truth dataset will therefore contain information such as:

- `transaction_id`
- `is_anomaly`
- `anomaly_type`
- `is_fraud`

These labels are **not provided to the anomaly detection models**.

They are only used after detection to evaluate model performance.

This enables comparison between:

- Rule-based detection
- Statistical detection
- Machine learning approaches

using metrics such as:

- Precision
- Recall
- F1-score
- False Positive Rate
- False Negative Rate
- Detection Rate

Accuracy will not be used as the primary metric because anomaly detection datasets are typically highly imbalanced.

---

# 19. Derived Customer Behaviour Profile

After generating the historical transactions, SQL will be used to calculate a behavioural profile for each customer.

The resulting `customer_behavior_profile` table may include:

### Spending behaviour

- Average transaction amount
- Median transaction amount
- Standard deviation
- 95th percentile transaction amount
- Maximum transaction amount
- Average monthly spending

### Transaction frequency

- Average transactions per month
- Average transactions per day
- Maximum transactions within a short period
- Average time between transactions

### Geographic behaviour

- Primary country
- Number of countries used
- International transaction rate
- Geographic distance from usual activity

### Merchant behaviour

- Most frequent merchant categories
- Number of merchant categories used
- Merchant category diversity
- New merchant rate

### Time behaviour

- Typical transaction hour
- Night-time transaction rate
- Weekend transaction rate

### Digital behaviour

- Online transaction rate
- Number of devices used
- Primary device
- New device frequency

These variables will later become important features for the anomaly detection engine.

---

# 20. Data Model

The initial data model is composed of the following tables:

```text
customers
    │
    │ 1:N
    ▼
transactions
    │
    ├──────────────► merchants
    │
    └──────────────► customer_behavior_profile
                             
transactions
    │
    ▼
fraud_alerts
    │
    ▼
customer_verifications
```