CREATE TABLE application (
    id INTEGER PRIMARY KEY,
    as_of_year SMALLINT NOT NULL,
    respondent_id TEXT NOT NULL,
    agency_code SMALLINT NOT NULL,
    loan_type SMALLINT NOT NULL,
    property_type SMALLINT NOT NULL,
    loan_purpose SMALLINT NOT NULL,
    owner_occupancy SMALLINT NOT NULL,
    loan_amount_000s INTEGER,
    preapproval SMALLINT NOT NULL,
    action_taken SMALLINT NOT NULL,
    msamd INTEGER,
    state_code SMALLINT NOT NULL,
    county_code INTEGER,
    census_tract_number DECIMAL(7,2),
    applicant_ethnicity SMALLINT NOT NULL,
    co_applicant_ethnicity SMALLINT NOT NULL,
    applicant_race_1 SMALLINT NOT NULL,
    applicant_race_2 SMALLINT,
    applicant_race_3 SMALLINT,
    applicant_race_4 SMALLINT,
    applicant_race_5 SMALLINT,
    co_applicant_race_1 SMALLINT NOT NULL,
    co_applicant_race_2 SMALLINT,
    co_applicant_race_3 SMALLINT,
    co_applicant_race_4 SMALLINT,
    co_applicant_race_5 SMALLINT,
    applicant_sex SMALLINT NOT NULL,
    co_applicant_sex SMALLINT NOT NULL,
    applicant_income_000s INTEGER,
    purchaser_type SMALLINT NOT NULL,
    denial_reason_1 SMALLINT,
    denial_reason_2 SMALLINT,
    denial_reason_3 SMALLINT,
    rate_spread DECIMAL(5,2),
    hoepa_status SMALLINT NOT NULL,
    lien_status SMALLINT NOT NULL,
    edit_status TEXT,
    sequence_number INTEGER,
    population INTEGER,
    minority_population DECIMAL(5,2),
    hud_median_family_income INTEGER,
    tract_to_msamd_income DECIMAL(5,2) NOT NULL,
    number_of_owner_occupied_units INTEGER NOT NULL,
    number_of_1_to_4_family_units INTEGER NOT NULL,
    application_date_indicator SMALLINT
);

INSERT INTO application
SELECT 
    id,
    NULLIF(as_of_year, '')::SMALLINT,
    NULLIF(respondent_id, ''),
    NULLIF(agency_code, '')::SMALLINT,
    NULLIF(loan_type, '')::SMALLINT,
    NULLIF(property_type, '')::SMALLINT,
    NULLIF(loan_purpose, '')::SMALLINT,
    NULLIF(owner_occupancy, '')::SMALLINT,
    CASE WHEN loan_amount_000s = '' THEN NULL ELSE loan_amount_000s::INTEGER END,
    NULLIF(preapproval, '')::SMALLINT,
    NULLIF(action_taken, '')::SMALLINT,
    CASE WHEN msamd = '' THEN NULL ELSE msamd::INTEGER END,
    NULLIF(state_code, '')::SMALLINT,
    CASE WHEN county_code = '' THEN NULL ELSE county_code::INTEGER END,
    CASE WHEN census_tract_number = '' THEN NULL ELSE census_tract_number::DECIMAL(7,2) END,
    NULLIF(applicant_ethnicity, '')::SMALLINT,
    NULLIF(co_applicant_ethnicity, '')::SMALLINT,
    NULLIF(applicant_race_1, '')::SMALLINT,
    CASE WHEN applicant_race_2 = '' THEN NULL ELSE applicant_race_2::SMALLINT END,
    CASE WHEN applicant_race_3 = '' THEN NULL ELSE applicant_race_3::SMALLINT END,
    CASE WHEN applicant_race_4 = '' THEN NULL ELSE applicant_race_4::SMALLINT END,
    CASE WHEN applicant_race_5 = '' THEN NULL ELSE applicant_race_5::SMALLINT END,
    NULLIF(co_applicant_race_1, '')::SMALLINT,
    CASE WHEN co_applicant_race_2 = '' THEN NULL ELSE co_applicant_race_2::SMALLINT END,
    CASE WHEN co_applicant_race_3 = '' THEN NULL ELSE co_applicant_race_3::SMALLINT END,
    CASE WHEN co_applicant_race_4 = '' THEN NULL ELSE co_applicant_race_4::SMALLINT END,
    CASE WHEN co_applicant_race_5 = '' THEN NULL ELSE co_applicant_race_5::SMALLINT END,
    NULLIF(applicant_sex, '')::SMALLINT,
    NULLIF(co_applicant_sex, '')::SMALLINT,
    CASE WHEN applicant_income_000s = '' THEN NULL ELSE applicant_income_000s::INTEGER END,
    NULLIF(purchaser_type, '')::SMALLINT,
    CASE WHEN denial_reason_1 = '' THEN NULL ELSE denial_reason_1::SMALLINT END,
    CASE WHEN denial_reason_2 = '' THEN NULL ELSE denial_reason_2::SMALLINT END,
    CASE WHEN denial_reason_3 = '' THEN NULL ELSE denial_reason_3::SMALLINT END,
    CASE WHEN rate_spread = '' THEN NULL ELSE rate_spread::DECIMAL(5,2) END,
    NULLIF(hoepa_status, '')::SMALLINT,
    NULLIF(lien_status, '')::SMALLINT,
    NULLIF(edit_status, ''),
    CASE WHEN sequence_number = '' THEN NULL ELSE sequence_number::INTEGER END,
    CASE WHEN population = '' THEN NULL ELSE population::INTEGER END,
    CASE WHEN minority_population = '' THEN NULL ELSE minority_population::DECIMAL(5,2) END,
    CASE WHEN hud_median_family_income = '' THEN NULL ELSE hud_median_family_income::INTEGER END,
    CASE WHEN tract_to_msamd_income = '' THEN NULL ELSE tract_to_msamd_income::DECIMAL(5,2) END,
    CASE WHEN number_of_owner_occupied_units = '' THEN NULL ELSE number_of_owner_occupied_units::INTEGER END,
    CASE WHEN number_of_1_to_4_family_units = '' THEN NULL ELSE number_of_1_to_4_family_units::INTEGER END,
    CASE WHEN application_date_indicator = '' THEN NULL ELSE application_date_indicator::SMALLINT END
FROM preliminary;

ALTER TABLE application ADD FOREIGN KEY (agency_code) REFERENCES agency(agency_code);
ALTER TABLE application ADD FOREIGN KEY (loan_type) REFERENCES loan_type(loan_type);
ALTER TABLE application ADD FOREIGN KEY (property_type) REFERENCES property_type(property_type);
ALTER TABLE application ADD FOREIGN KEY (owner_occupancy) REFERENCES owner_occupancy(owner_occupancy);
ALTER TABLE application ADD FOREIGN KEY (preapproval) REFERENCES preapproval(preapproval);
ALTER TABLE application ADD FOREIGN KEY (action_taken) REFERENCES action_taken(action_taken);
ALTER TABLE application ADD FOREIGN KEY (msamd) REFERENCES msamd(msamd);
ALTER TABLE application ADD FOREIGN KEY (state_code) REFERENCES state(state_code);
ALTER TABLE application ADD FOREIGN KEY (county_code) REFERENCES county(county_code);
ALTER TABLE application ADD FOREIGN KEY (applicant_ethnicity) REFERENCES ethnicity(ethnicity_code);
ALTER TABLE application ADD FOREIGN KEY (co_applicant_ethnicity) REFERENCES ethnicity(ethnicity_code);
ALTER TABLE application ADD FOREIGN KEY (applicant_race_1) REFERENCES race(race_code);
ALTER TABLE application ADD FOREIGN KEY (applicant_race_2) REFERENCES race(race_code);
ALTER TABLE application ADD FOREIGN KEY (applicant_race_3) REFERENCES race(race_code);
ALTER TABLE application ADD FOREIGN KEY (applicant_race_4) REFERENCES race(race_code);
ALTER TABLE application ADD FOREIGN KEY (applicant_race_5) REFERENCES race(race_code);
ALTER TABLE application ADD FOREIGN KEY (co_applicant_race_1) REFERENCES race(race_code);
ALTER TABLE application ADD FOREIGN KEY (co_applicant_race_2) REFERENCES race(race_code);
ALTER TABLE application ADD FOREIGN KEY (co_applicant_race_3) REFERENCES race(race_code);
ALTER TABLE application ADD FOREIGN KEY (co_applicant_race_4) REFERENCES race(race_code);
ALTER TABLE application ADD FOREIGN KEY (co_applicant_race_5) REFERENCES race(race_code);
ALTER TABLE application ADD FOREIGN KEY (applicant_sex) REFERENCES sex(sex_code);
ALTER TABLE application ADD FOREIGN KEY (co_applicant_sex) REFERENCES sex(sex_code);
ALTER TABLE application ADD FOREIGN KEY (purchaser_type) REFERENCES purchaser_type(purchaser_type);
ALTER TABLE application ADD FOREIGN KEY (denial_reason_1) REFERENCES denial_reason(denial_reason_code);
ALTER TABLE application ADD FOREIGN KEY (denial_reason_2) REFERENCES denial_reason(denial_reason_code);
ALTER TABLE application ADD FOREIGN KEY (denial_reason_3) REFERENCES denial_reason(denial_reason_code);
ALTER TABLE application ADD FOREIGN KEY (hoepa_status) REFERENCES hoepa_status(hoepa_status);
ALTER TABLE application ADD FOREIGN KEY (lien_status) REFERENCES lien_status(lien_status);

