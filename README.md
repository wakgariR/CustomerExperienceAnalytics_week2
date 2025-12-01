# CustomerExperienceAnalytics_week2

#### Steps for create bank_reviews database and create Banks Reviews tables

- database with with **bank_revies** cratead
  ![alt text](image.png)
  then open the scritp termian and excute below query to crate both table

- To create banks table use this query

```
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(255) NOT NULL,
    app_name VARCHAR(255)
);
```

- use this script to inser our three banks

```
INSERT INTO banks (bank_name, app_name)
VALUES
    ('CBE', 'Commercial Bank of Ethiopia'),
    ('BoAMobile', 'BoA Mobile'),
    ('DashenBank', 'Dashen Bank');
```

- To create reviews use this query

```
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT NOT NULL,
    review_text TEXT,
    rating INT,
    review_date DATE,
    sentiment_label VARCHAR(50),
    sentiment_score DECIMAL(5,2),
    source VARCHAR(100),
    CONSTRAINT fk_bank
        FOREIGN KEY (bank_id)
        REFERENCES banks (bank_id)
        ON DELETE CASCADE
);
```
