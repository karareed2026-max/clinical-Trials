#!/usr/bin/env python3
"""
Precompute fast summary datasets from aact_trial_termination_candidate_2026-09-12.tsv.gz
for interactive Quarto reporting across all pages.
"""

import gzip
import csv
import math
from collections import defaultdict, Counter

SOURCE_PATH = "data/processed/aact_trial_termination_candidate_2026-09-12.tsv.gz"

def categorize_reason(text):
    t = (text or "").lower().strip()
    if not t or t == "[missing]":
        return None
    if any(k in t for k in ['accrual', 'enroll', 'recruit', 'patient', 'participant', 'subject', 'insufficient accrual', 'slow accrual', 'poor accrual', 'low enrollment', 'no participants']):
        return 'Accrual & Recruitment Bottlenecks'
    elif any(k in t for k in ['sponsor', 'fund', 'business', 'financial', 'commercial', 'strategic', 'company', 'budget', 'priorit']):
        return 'Business, Funding & Strategic Decisions'
    elif any(k in t for k in ['futil', 'efficac', 'endpoint', 'benefit', 'no effect', 'ineffective', 'interim analysis', 'failed to show']):
        return 'Lack of Efficacy & Futility'
    elif any(k in t for k in ['safe', 'toxic', 'adverse', 'death', 'side effect', 'risk', 'harm', 'dlt']):
        return 'Safety & Adverse Events'
    elif any(k in t for k in ['pi ', 'investigator', 'staff', 'faculty', 'leave', 'left', 'retirement', 'departure']):
        return 'Investigator Departure & Staffing'
    elif any(k in t for k in ['covid', 'pandemic', 'coronavirus']):
        return 'External Shocks (COVID-19 / Logistics)'
    elif any(k in t for k in ['drug', 'product', 'supply', 'manufacturer', 'manufacturing', 'formulation', 'lot']):
        return 'Drug Supply & Manufacturing'
    elif any(k in t for k in ['regulatory', 'fda', 'irb', 'approval', 'compliance', 'protocol']):
        return 'Regulatory & Protocol Compliance'
    else:
        return 'Other Administrative & Operational'

def get_era(year):
    if year < 2000:
        return "1990–1999"
    elif year < 2010:
        return "2000–2009"
    elif year < 2020:
        return "2010–2019"
    else:
        return "2020–2026"

def get_phase_display(phase):
    if phase in ["PHASE1", "EARLY_PHASE1"]:
        return "Phase I"
    elif phase == "PHASE2":
        return "Phase II"
    elif phase == "PHASE3":
        return "Phase III"
    elif phase == "PHASE4":
        return "Phase IV"
    elif phase == "NA":
        return "Not applicable"
    elif phase in ["PHASE1/PHASE2", "PHASE2/PHASE3"]:
        return "Mixed Phase (I/II or II/III)"
    else:
        return "Other / Missing"

def get_sponsor_label(stype):
    mapping = {
        "OTHER": "Academic & Hospital Systems",
        "INDUSTRY": "Industry (Pharma / Biotech)",
        "OTHER_GOV": "Other Government (State / Non-US)",
        "NIH": "National Institutes of Health (NIH)",
        "NETWORK": "Research Networks",
        "FED": "US Federal Agencies (VA / DoD)",
        "INDIV": "Individual Investigators",
        "[missing]": "Not Reported",
        "UNKNOWN": "Unknown"
    }
    return mapping.get(stype, "Other")

def get_site_category(num_sites_str):
    try:
        sites = int(num_sites_str)
        if sites == 0:
            return "0 sites / Not reported"
        elif sites == 1:
            return "Single-site (1)"
        elif 2 <= sites <= 5:
            return "Small multi-site (2–5)"
        elif 6 <= sites <= 20:
            return "Medium multi-site (6–20)"
        elif 21 <= sites <= 50:
            return "Large multi-site (21–50)"
        else:
            return "Global mega-network (51+)"
    except (ValueError, TypeError):
        return "Not reported"

def classify_therapeutic_area(cond):
    c = (cond or '').lower()
    if not c or c == '[missing]':
        return 'Unspecified / Missing'
    if any(k in c for k in ['healthy', 'normal volunteer']):
        return 'Healthy Volunteers'
    if any(k in c for k in ['cancer', 'neoplasm', 'carcinoma', 'tumor', 'tumour', 'leukemia', 'lymphoma', 'melanoma', 'sarcoma', 'oncolog', 'myeloma', 'blast']):
        return 'Oncology / Cancer'
    if any(k in c for k in ['heart', 'coronary', 'hypertens', 'cardio', 'myocardi', 'arrhythm', 'stroke', 'atrial', 'thrombos', 'vascular', 'ischemi', 'arterial']):
        return 'Cardiovascular & Vascular'
    if any(k in c for k in ['depress', 'schizophr', 'anxiet', 'bipolar', 'psych', 'addict', 'alcohol', 'substance', 'ptsd', 'autism', 'adhd', 'panic']):
        return 'Psychiatry & Mental Health'
    if any(k in c for k in ['alzheimer', 'parkinson', 'neurolog', 'epilep', 'seizure', 'sclerosis', 'dementia', 'migraine', 'headache', 'brain', 'spinal cord', 'tremor', 'als']):
        return 'Neurology & CNS'
    if any(k in c for k in ['hiv', 'covid', 'infect', 'hepatit', 'virus', 'viral', 'bacteria', 'sepsis', 'tubercul', 'pneumonia', 'fungal', 'vaccin']):
        return 'Infectious Diseases'
    if any(k in c for k in ['diabet', 'obes', 'thyroid', 'metabol', 'glucose', 'lipid', 'cholesterol', 'endocrine', 'hyperglyc']):
        return 'Metabolic & Endocrine'
    if any(k in c for k in ['asthma', 'copd', 'pulmon', 'respirat', 'lung', 'bronch', 'cystic fibros']):
        return 'Respiratory & Pulmonology'
    if any(k in c for k in ['gastro', 'colitis', 'crohn', 'bowel', 'liver', 'hepat', 'cirrhos', 'ulcer', 'pancreat', 'gastric', 'esophag']):
        return 'Gastroenterology & Hepatology'
    if any(k in c for k in ['immun', 'autoimmun', 'lupus', 'arthrit', 'rheumat', 'psoria']):
        return 'Immunology & Rheumatology'
    if any(k in c for k in ['eye', 'ocular', 'retin', 'glaucoma', 'macul', 'cataract', 'cornea', 'uveit', 'ophthalm', 'vision']):
        return 'Ophthalmology'
    if any(k in c for k in ['dermat', 'skin', 'eczema', 'acne', 'cutan']):
        return 'Dermatology'
    if any(k in c for k in ['renal', 'kidney', 'nephr', 'dialysis', 'urinary', 'bladder', 'prostat']):
        return 'Nephrology & Urology'
    if any(k in c for k in ['pain', 'analges']):
        return 'Pain & Anesthesiology'
    return 'Other Conditions / Rare Diseases'

print("Parsing candidate dataset...")

# Data structures
annual_enrollments = defaultdict(list)
era_enrollments = defaultdict(list)
why_stopped_counter = Counter()
status_counter = Counter()
status_terminated_counter = Counter()
phase_stats = defaultdict(lambda: {"total": 0, "terminated": 0})
sponsor_stats = defaultdict(lambda: {"total": 0, "terminated": 0})
design_stats = defaultdict(lambda: {"total": 0, "terminated": 0})
site_stats = defaultdict(lambda: {"total": 0, "terminated": 0})

# New requested signals
area_stats = defaultdict(lambda: {"total": 0, "terminated": 0})
intervention_stats = defaultdict(lambda: {"total": 0, "terminated": 0})
duration_stats = defaultdict(lambda: {"total": 0, "terminated": 0})
rand_stats = defaultdict(lambda: {"total": 0, "terminated": 0})
placebo_stats = defaultdict(lambda: {"total": 0, "terminated": 0})
complexity_stats = defaultdict(lambda: {"total": 0, "terminated": 0})
condition_count_stats = defaultdict(lambda: {"total": 0, "terminated": 0})

total_trials = 0

with gzip.open(SOURCE_PATH, "rt") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        total_trials += 1
        status = row["overall_status"]
        status_counter[status] += 1
        is_terminated = (row["terminated_binary"] == "1")
        if is_terminated:
            status_terminated_counter[status] += 1

        # Reason stopped
        if is_terminated:
            why = row.get("why_stopped", "")
            cat = categorize_reason(why)
            if cat:
                why_stopped_counter[cat] += 1

        # Phase
        p_disp = get_phase_display(row.get("phase", ""))
        phase_stats[p_disp]["total"] += 1
        if is_terminated:
            phase_stats[p_disp]["terminated"] += 1

        # Sponsor
        s_label = get_sponsor_label(row.get("lead_sponsor_type", ""))
        sponsor_stats[s_label]["total"] += 1
        if is_terminated:
            sponsor_stats[s_label]["terminated"] += 1

        # Design
        rand_val = row.get("randomized_vs_nonrandomized", "not reported")
        d_group = "Randomized" if rand_val == "randomized" else ("Non-randomized" if rand_val == "non-randomized" else "Not reported")
        plac_val = row.get("placebo_used", "not reported")
        p_group = "Placebo mentioned" if plac_val == "yes" else ("No placebo found" if plac_val == "no" else "Not reported")
        design_key = (d_group, p_group)
        design_stats[design_key]["total"] += 1
        if is_terminated:
            design_stats[design_key]["terminated"] += 1

        # Sites
        s_cat = get_site_category(row.get("number_of_sites", ""))
        site_stats[s_cat]["total"] += 1
        if is_terminated:
            site_stats[s_cat]["terminated"] += 1

        # Enrollment
        try:
            start_yr = int(row.get("start_year", ""))
            enr = float(row.get("enrollment", ""))
            if 1990 <= start_yr <= 2026 and enr > 0:
                annual_enrollments[start_yr].append(enr)
                era_enrollments[get_era(start_yr)].append(enr)
        except (ValueError, TypeError):
            pass

        # 1. Therapeutic Area
        cond_text = (row.get("primary_condition") or "") + " " + (row.get("conditions_all") or "")
        area = classify_therapeutic_area(cond_text)
        area_stats[area]["total"] += 1
        if is_terminated:
            area_stats[area]["terminated"] += 1

        # 2. Number of Interventions
        try:
            ic = int(row.get("intervention_count", 0))
            if ic == 0: ic_label = "0 (Observational/None)"
            elif ic == 1: ic_label = "1 intervention"
            elif ic == 2: ic_label = "2 interventions"
            elif ic == 3: ic_label = "3 interventions"
            elif ic == 4: ic_label = "4 interventions"
            else: ic_label = "5+ interventions"
        except (ValueError, TypeError):
            ic_label = "Not reported"
            ic = 0
        intervention_stats[ic_label]["total"] += 1
        if is_terminated:
            intervention_stats[ic_label]["terminated"] += 1

        # 3. Randomization
        rand_stats[d_group]["total"] += 1
        if is_terminated:
            rand_stats[d_group]["terminated"] += 1

        # 4. Placebo
        plac_raw = (row.get("placebo_used") or "").strip().lower()
        if plac_raw == "yes": plac_label = "Placebo control used"
        elif plac_raw == "no": plac_label = "No placebo reported"
        else: plac_label = "Not reported"
        placebo_stats[plac_label]["total"] += 1
        if is_terminated:
            placebo_stats[plac_label]["terminated"] += 1

        # 5. Study Duration Brackets
        try:
            dur = int(row.get("study_duration_days", ""))
            if 0 < dur < 365 * 25:
                if dur < 180: dur_label = "< 6 months"
                elif dur < 365: dur_label = "6–12 months"
                elif dur < 365 * 2: dur_label = "1–2 years"
                elif dur < 365 * 3: dur_label = "2–3 years"
                elif dur < 365 * 5: dur_label = "3–5 years"
                else: dur_label = "5+ years"
                duration_stats[dur_label]["total"] += 1
                if is_terminated:
                    duration_stats[dur_label]["terminated"] += 1
        except (ValueError, TypeError):
            pass

        # 6. Number of Conditions
        cond_str = (row.get("conditions_all") or "").strip()
        if not cond_str or cond_str == "[missing]":
            cond_cat = "0 / Missing"
        else:
            items = [x.strip() for x in cond_str.replace("|", ",").split(",") if x.strip()]
            n_c = len(items)
            if n_c <= 1: cond_cat = "1 condition"
            elif n_c == 2: cond_cat = "2 conditions"
            elif 3 <= n_c <= 4: cond_cat = "3–4 conditions"
            else: cond_cat = "5+ conditions"
        condition_count_stats[cond_cat]["total"] += 1
        if is_terminated:
            condition_count_stats[cond_cat]["terminated"] += 1

        # 7. Study Complexity Score
        score = 0
        try:
            arms = int(row.get("number_of_arms", 0))
            if arms >= 3: score += 1
        except: pass
        if ic >= 3: score += 1
        if plac_raw == "yes": score += 1
        mask = (row.get("masking") or "").upper()
        if any(m in mask for m in ["DOUBLE", "TRIPLE", "QUADRUPLE"]): score += 1
        try:
            sites = int(row.get("number_of_sites", 0))
            if sites >= 6: score += 1
        except: pass
        try:
            outcomes = int(row.get("primary_outcome_count", 0))
            if outcomes >= 3: score += 1
        except: pass

        if score <= 1: comp_label = "Low Complexity (0–1)"
        elif score == 2: comp_label = "Moderate Complexity (2)"
        elif score == 3: comp_label = "High Complexity (3)"
        else: comp_label = "Very High Complexity (4+)"
        complexity_stats[comp_label]["total"] += 1
        if is_terminated:
            complexity_stats[comp_label]["terminated"] += 1

print(f"Parsed {total_trials:,} trials.")

# Write annual enrollment summary
with open("data/processed/summary_annual_enrollment.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["start_year", "studies", "lower", "median", "upper", "mean"])
    for yr in sorted(annual_enrollments.keys()):
        arr = sorted(annual_enrollments[yr])
        n = len(arr)
        q25 = arr[int(0.25 * n)]
        med = arr[int(0.50 * n)]
        q75 = arr[int(0.75 * n)]
        mean_val = sum(arr) / n
        writer.writerow([yr, n, round(q25, 1), round(med, 1), round(q75, 1), round(mean_val, 1)])

# Write era histogram summary
log_breaks = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 50000, 1000000]
bin_labels = [
    "1–4", "5–9", "10–24", "25–49", "50–99", "100–249", "250–499",
    "500–999", "1,000–2,499", "2,500–4,999", "5,000–9,999", "10,000–49,999", "50,000+"
]

def bin_values(values):
    counts = [0] * (len(log_breaks) - 1)
    for v in values:
        for i in range(len(log_breaks) - 1):
            if log_breaks[i] <= v < log_breaks[i+1]:
                counts[i] += 1
                break
            elif i == len(log_breaks) - 2 and v >= log_breaks[i+1]:
                counts[i] += 1
                break
    return counts

with open("data/processed/summary_enrollment_histograms.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["era", "bin_index", "bin_label", "bin_min", "bin_max", "count", "pct", "total_in_era"])
    for era in ["1990–1999", "2000–2009", "2010–2019", "2020–2026"]:
        arr = era_enrollments[era]
        tot = len(arr)
        counts = bin_values(arr)
        for i, c in enumerate(counts):
            pct = (c / tot * 100) if tot > 0 else 0
            writer.writerow([era, i, bin_labels[i], log_breaks[i], log_breaks[i+1], c, round(pct, 2), tot])

# Write why stopped summary
with open("data/processed/summary_why_stopped.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["category", "count", "percentage"])
    total_reasons = sum(why_stopped_counter.values())
    for cat, cnt in why_stopped_counter.most_common():
        pct = (cnt / total_reasons * 100) if total_reasons > 0 else 0
        writer.writerow([cat, cnt, round(pct, 2)])

# Write phase summary
with open("data/processed/summary_phase.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["phase_display", "total_studies", "terminated_studies", "termination_rate"])
    for p, stats in sorted(phase_stats.items(), key=lambda x: x[1]["total"], reverse=True):
        rate = (stats["terminated"] / stats["total"]) if stats["total"] > 0 else 0
        writer.writerow([p, stats["total"], stats["terminated"], round(rate, 4)])

# Write sponsor summary
with open("data/processed/summary_sponsors.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["sponsor_label", "total_studies", "terminated_studies", "termination_rate"])
    for s, stats in sorted(sponsor_stats.items(), key=lambda x: x[1]["total"], reverse=True):
        rate = (stats["terminated"] / stats["total"]) if stats["total"] > 0 else 0
        writer.writerow([s, stats["total"], stats["terminated"], round(rate, 4)])

# Write design summary
with open("data/processed/summary_design.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["design_group", "placebo_used", "total_studies", "terminated_studies", "termination_rate"])
    for (d, p), stats in sorted(design_stats.items(), key=lambda x: x[1]["total"], reverse=True):
        rate = (stats["terminated"] / stats["total"]) if stats["total"] > 0 else 0
        writer.writerow([d, p, stats["total"], stats["terminated"], round(rate, 4)])

# Write sites summary
with open("data/processed/summary_sites.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["site_category", "total_studies", "terminated_studies", "termination_rate"])
    for s, stats in sorted(site_stats.items(), key=lambda x: x[1]["total"], reverse=True):
        rate = (stats["terminated"] / stats["total"]) if stats["total"] > 0 else 0
        writer.writerow([s, stats["total"], stats["terminated"], round(rate, 4)])

# Write status summary
with open("data/processed/summary_status.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["overall_status", "studies", "terminated_count", "pct_of_total"])
    for status, cnt in status_counter.most_common():
        pct = (cnt / total_trials * 100) if total_trials > 0 else 0
        term_cnt = status_terminated_counter[status]
        writer.writerow([status, cnt, term_cnt, round(pct, 2)])

# 1. Write Therapeutic Area summary (Home page)
with open("data/processed/summary_therapeutic_areas.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["therapeutic_area", "total_studies", "terminated_studies", "termination_rate", "pct_of_all_trials"])
    for a, stats in sorted(area_stats.items(), key=lambda x: x[1]["total"], reverse=True):
        rate = (stats["terminated"] / stats["total"]) if stats["total"] > 0 else 0
        pct = (stats["total"] / total_trials * 100) if total_trials > 0 else 0
        writer.writerow([a, stats["total"], stats["terminated"], round(rate, 4), round(pct, 2)])

# 2. Write Interventions summary (Termination Signals)
with open("data/processed/summary_interventions.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["intervention_label", "total_studies", "terminated_studies", "termination_rate"])
    int_order = ["0 (Observational/None)", "1 intervention", "2 interventions", "3 interventions", "4 interventions", "5+ interventions"]
    for lbl in int_order:
        stats = intervention_stats[lbl]
        rate = (stats["terminated"] / stats["total"]) if stats["total"] > 0 else 0
        writer.writerow([lbl, stats["total"], stats["terminated"], round(rate, 4)])

# 3. Write Duration summary (Termination Signals)
with open("data/processed/summary_durations.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["duration_bracket", "total_studies", "terminated_studies", "termination_rate"])
    dur_order = ["< 6 months", "6–12 months", "1–2 years", "2–3 years", "3–5 years", "5+ years"]
    for lbl in dur_order:
        stats = duration_stats[lbl]
        rate = (stats["terminated"] / stats["total"]) if stats["total"] > 0 else 0
        writer.writerow([lbl, stats["total"], stats["terminated"], round(rate, 4)])

# 4. Write Randomization summary (Termination Signals)
with open("data/processed/summary_randomization.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["randomization_status", "total_studies", "terminated_studies", "termination_rate"])
    for r, stats in sorted(rand_stats.items(), key=lambda x: x[1]["total"], reverse=True):
        rate = (stats["terminated"] / stats["total"]) if stats["total"] > 0 else 0
        writer.writerow([r, stats["total"], stats["terminated"], round(rate, 4)])

# 5. Write Placebo summary (Termination Signals)
with open("data/processed/summary_placebo.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["placebo_status", "total_studies", "terminated_studies", "termination_rate"])
    for p, stats in sorted(placebo_stats.items(), key=lambda x: x[1]["total"], reverse=True):
        rate = (stats["terminated"] / stats["total"]) if stats["total"] > 0 else 0
        writer.writerow([p, stats["total"], stats["terminated"], round(rate, 4)])

# 6. Write Complexity summary (Termination Signals)
with open("data/processed/summary_complexity.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["complexity_tier", "total_studies", "terminated_studies", "termination_rate"])
    comp_order = ["Low Complexity (0–1)", "Moderate Complexity (2)", "High Complexity (3)", "Very High Complexity (4+)"]
    for lbl in comp_order:
        stats = complexity_stats[lbl]
        rate = (stats["terminated"] / stats["total"]) if stats["total"] > 0 else 0
        writer.writerow([lbl, stats["total"], stats["terminated"], round(rate, 4)])

# 7. Write Conditions Count summary (Termination Signals)
with open("data/processed/summary_conditions_count.tsv", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["conditions_category", "total_studies", "terminated_studies", "termination_rate"])
    cond_order = ["1 condition", "2 conditions", "3–4 conditions", "5+ conditions", "0 / Missing"]
    for lbl in cond_order:
        stats = condition_count_stats[lbl]
        rate = (stats["terminated"] / stats["total"]) if stats["total"] > 0 else 0
        writer.writerow([lbl, stats["total"], stats["terminated"], round(rate, 4)])

print("Successfully generated all summary tables!")
