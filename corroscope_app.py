
from datetime import date

import pandas as pd  # type: ignore
import streamlit as st

from calculations import (
    calculate_electrochemical_corrosion_rate,
    calculate_inhibition_efficiency,
    calculate_mass_loss,
    calculate_weight_loss_corrosion_rate,
)


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="CorroScope | Corrosion Research",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# VISUAL DESIGN
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #ffffff;
    }

    [data-testid="stSidebar"] {
        background: #f5f7fb;
        border-right: 1px solid #e6ebf2;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }

    .brand {
        color: #172b4d;
        font-size: 1.45rem;
        font-weight: 700;
        letter-spacing: -0.04em;
    }

    .brand-sub {
        color: #66758c;
        font-size: 0.82rem;
        margin-top: 0.15rem;
    }

    .eyebrow {
        color: #356ae6;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .hero-title {
        color: #142b50;
        font-size: clamp(2rem, 4vw, 3.1rem);
        line-height: 1.13;
        font-weight: 700;
        letter-spacing: -0.055em;
        margin: 0.45rem 0 0.8rem 0;
    }

    .hero-copy {
        color: #5c6c83;
        font-size: 1rem;
        line-height: 1.75;
        max-width: 800px;
    }

    .muted {
        color: #66758c;
        font-size: 0.88rem;
        line-height: 1.65;
    }

    div[data-testid="stMetric"] {
        background: #f5f7fb;
        border: 1px solid #e6ebf2;
        border-radius: 12px;
        padding: 0.9rem 1rem;
    }

    div[data-testid="stForm"] {
        border: 1px solid #e6ebf2;
        border-radius: 14px;
        padding: 1.2rem;
    }

    .stButton button,
    .stDownloadButton button {
        border-radius: 9px;
        font-weight: 600;
    }

    h1, h2, h3 {
        color: #172b4d;
        letter-spacing: -0.035em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "experiments" not in st.session_state:
    st.session_state.experiments = []

if "literature_notes" not in st.session_state:
    st.session_state.literature_notes = []

if "last_weight_result" not in st.session_state:
    st.session_state.last_weight_result = None

if "last_electro_result" not in st.session_state:
    st.session_state.last_electro_result = None

NAV_ITEMS = [
    "Home",
    "Weight Loss Analysis",
    "Electrochemical Analysis",
    "Inhibition Efficiency",
    "Data & Experiments",
    "Literature Notes",
    "About & Navigation",
]

if "navigation" not in st.session_state:
    st.session_state.navigation = "Home"


# ---------------------------------------------------------
# REUSABLE HELPERS
# ---------------------------------------------------------

def page_header(section, title, description):
    st.markdown(
        f'<div class="eyebrow">{section}</div>',
        unsafe_allow_html=True,
    )
    st.title(title)
    st.markdown(
        f'<div class="muted">{description}</div>',
        unsafe_allow_html=True,
    )
    st.write("")


def records_dataframe():
    return pd.DataFrame(st.session_state.experiments)


def add_experiment_record(record):
    """Add one record to the active Streamlit session."""
    st.session_state.experiments.append(record)


def navigate_to(target):
    st.session_state.navigation = target
    st.rerun()


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------

with st.sidebar:
    st.markdown(
        '<div class="brand">⚗️ CorroScope</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="brand-sub">Corrosion research workspace</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.radio(
        "WORKSPACE",
        NAV_ITEMS,
        key="navigation",
    )

    st.divider()

    st.caption("Research tools · Calculations · Records")
    st.caption("Version 1.0")


page = st.session_state.navigation


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

if page == "Home":

    st.markdown(
        '<div class="eyebrow">CORROSION RESEARCH WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-title">
            Turn experimental measurements<br>
            into clear, traceable results.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-copy">
            CorroScope helps corrosion researchers calculate selected
            corrosion metrics, compare inhibitor performance, and organize
            laboratory measurements in one workspace.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("⚖️ Weight-loss analysis")
        st.markdown(
            '<div class="muted">Calculate mass loss and gravimetric corrosion rate.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Open weight-loss tools", use_container_width=True):
            navigate_to("Weight Loss Analysis")

    with col2:
        st.subheader("⚡ Electrochemical analysis")
        st.markdown(
            '<div class="muted">Estimate corrosion rate from corrosion current density.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Open electrochemical tools", use_container_width=True):
            navigate_to("Electrochemical Analysis")

    with col3:
        st.subheader("🗂️ Experiment records")
        st.markdown(
            '<div class="muted">Review, import, and export experimental records.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Open experiment log", use_container_width=True):
            navigate_to("Data & Experiments")

    st.write("")
    st.subheader("Workspace overview")

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Experiment records",
        len(st.session_state.experiments),
    )

    metric2.metric(
        "Literature notes",
        len(st.session_state.literature_notes),
    )

    metric3.metric(
        "Calculation tools",
        "4",
    )

    st.caption(
        "This version stores records in the active session. "
        "Export important records before ending the session."
    )


# ---------------------------------------------------------
# WEIGHT-LOSS ANALYSIS
# ---------------------------------------------------------

elif page == "Weight Loss Analysis":

    page_header(
        "GRAVIMETRIC METHOD",
        "Weight Loss Analysis",
        "Calculate specimen mass loss and estimate corrosion rate from gravimetric measurements.",
    )

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:

        st.subheader("Specimen measurements")

        with st.form("weight_loss_form"):

            col1, col2 = st.columns(2)

            initial_mass = col1.number_input(
                "Initial mass (g)",
                min_value=0.0,
                value=10.000,
                step=0.001,
                format="%.4f",
            )

            final_mass = col2.number_input(
                "Final mass after exposure (g)",
                min_value=0.0,
                value=9.800,
                step=0.001,
                format="%.4f",
            )

            st.subheader("Exposure conditions")

            col3, col4 = st.columns(2)

            density = col3.number_input(
                "Material density (g/cm³)",
                min_value=0.0001,
                value=7.85,
                step=0.05,
                format="%.4f",
            )

            area = col4.number_input(
                "Total exposed area (cm²)",
                min_value=0.0001,
                value=10.0,
                step=0.5,
                format="%.4f",
            )

            exposure_time = st.number_input(
                "Exposure time (hours)",
                min_value=0.0001,
                value=24.0,
                step=1.0,
                format="%.4f",
            )

            st.caption(
                "Include all specimen surfaces exposed to the medium, "
                "including faces and edges where applicable."
            )

            calculate_button = st.form_submit_button(
                "Calculate results",
                type="primary",
                use_container_width=True,
            )

        if calculate_button:
            try:
                mass_loss = calculate_mass_loss(
                    initial_mass,
                    final_mass,
                )

                corrosion_rate = calculate_weight_loss_corrosion_rate(
                    mass_loss,
                    density,
                    area,
                    exposure_time,
                )

                st.session_state.last_weight_result = {
                    "initial_mass_g": initial_mass,
                    "final_mass_g": final_mass,
                    "mass_loss_g": mass_loss,
                    "density_g_cm3": density,
                    "exposed_area_cm2": area,
                    "exposure_time_h": exposure_time,
                    "corrosion_rate_mm_year": corrosion_rate,
                }

            except (TypeError, ValueError) as error:
                st.error(str(error))

    with right:

        st.subheader("Results")

        result = st.session_state.last_weight_result

        if result is None:
            st.info(
                "Enter your measurements and select "
                "**Calculate results** to see your results."
            )

            st.markdown("**Weight-loss corrosion-rate equation**")

            st.latex(
                r"CR = \frac{87.6\,W}{\rho A t}"
            )

            st.markdown(
                """
                <div class="muted">
                W = mass loss in mg; ρ = density in g/cm³;
                A = exposed area in cm²; t = exposure time in hours.
                The result is in mm/year.
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:
            result_col1, result_col2 = st.columns(2)

            result_col1.metric(
                "Mass loss",
                f"{result['mass_loss_g']:.5f} g",
            )

            result_col2.metric(
                "Mass loss",
                f"{result['mass_loss_g'] * 1000:.3f} mg",
            )

            st.metric(
                "Corrosion rate",
                f"{result['corrosion_rate_mm_year']:.5f} mm/year",
            )

            st.markdown("#### Calculation details")

            st.code(
                f"Mass loss = {result['mass_loss_g']:.6f} g\n"
                f"Mass loss = {result['mass_loss_g'] * 1000:.4f} mg\n"
                f"Density = {result['density_g_cm3']:.4f} g/cm³\n"
                f"Exposed area = {result['exposed_area_cm2']:.4f} cm²\n"
                f"Exposure time = {result['exposure_time_h']:.4f} h\n"
                f"Corrosion rate = "
                f"{result['corrosion_rate_mm_year']:.5f} mm/year",
                language="text",
            )

            if st.button(
                "Save result to experiment log",
                type="secondary",
                use_container_width=True,
            ):
                record = {
                    "recorded_on": date.today().isoformat(),
                    "experiment_id": (
                        f"EXP-{len(st.session_state.experiments) + 1:04d}"
                    ),
                    "method": "Weight loss",
                    "specimen": "Not specified",
                    "medium": "Not specified",
                    **result,
                    "notes": "Saved from Weight Loss Analysis",
                }

                add_experiment_record(record)
                st.success("Result saved to the current session's experiment log.")

    st.warning(
        "Scientific note: mass loss should be measured after an appropriate "
        "specimen-cleaning procedure. Deposits, cleaning losses, and incorrect "
        "surface-area estimates can affect the result."
    )


# ---------------------------------------------------------
# ELECTROCHEMICAL ANALYSIS
# ---------------------------------------------------------

elif page == "Electrochemical Analysis":

    page_header(
        "ELECTROCHEMICAL METHOD",
        "Electrochemical Analysis",
        "Estimate corrosion rate using corrosion current density and equivalent weight.",
    )

    left, right = st.columns(2, gap="large")

    with left:

        with st.form("electrochemical_form"):

            current_density = st.number_input(
                "Corrosion current density, Icorr (µA/cm²)",
                min_value=0.0,
                value=10.0,
                step=0.5,
                format="%.5f",
            )

            equivalent_weight = st.number_input(
                "Equivalent weight (g/equivalent)",
                min_value=0.0001,
                value=27.92,
                step=0.1,
                format="%.4f",
            )

            electro_density = st.number_input(
                "Material density (g/cm³)",
                min_value=0.0001,
                value=7.85,
                step=0.05,
                format="%.4f",
            )

            electro_button = st.form_submit_button(
                "Calculate corrosion rate",
                type="primary",
                use_container_width=True,
            )

        if electro_button:
            try:
                rate = calculate_electrochemical_corrosion_rate(
                    current_density,
                    equivalent_weight,
                    electro_density,
                )

                st.session_state.last_electro_result = {
                    "current_density_uA_cm2": current_density,
                    "equivalent_weight_g_equiv": equivalent_weight,
                    "density_g_cm3": electro_density,
                    "corrosion_rate_mm_year": rate,
                }

            except (TypeError, ValueError) as error:
                st.error(str(error))

    with right:

        st.subheader("Results")

        result = st.session_state.last_electro_result

        if result is None:
            st.info("Enter the parameters and calculate the corrosion rate.")

            st.latex(
                r"CR = \frac{0.00327\,I_{\mathrm{corr}}\,EW}{\rho}"
            )

        else:
            st.metric(
                "Estimated corrosion rate",
                f"{result['corrosion_rate_mm_year']:.5f} mm/year",
            )

            st.markdown("#### Calculation details")

            st.code(
                f"Icorr = {result['current_density_uA_cm2']:.5f} µA/cm²\n"
                f"Equivalent weight = "
                f"{result['equivalent_weight_g_equiv']:.4f} g/equivalent\n"
                f"Density = {result['density_g_cm3']:.4f} g/cm³\n"
                f"Corrosion rate = "
                f"{result['corrosion_rate_mm_year']:.5f} mm/year",
                language="text",
            )

            if st.button("Save result to experiment log"):
                record = {
                    "recorded_on": date.today().isoformat(),
                    "experiment_id": (
                        f"EXP-{len(st.session_state.experiments) + 1:04d}"
                    ),
                    "method": "Electrochemical",
                    "specimen": "Not specified",
                    "medium": "Not specified",
                    "initial_mass_g": None,
                    "final_mass_g": None,
                    "mass_loss_g": None,
                    "density_g_cm3": result["density_g_cm3"],
                    "exposed_area_cm2": None,
                    "exposure_time_h": None,
                    "corrosion_rate_mm_year": result[
                        "corrosion_rate_mm_year"
                    ],
                    "notes": (
                        f"Icorr={result['current_density_uA_cm2']} µA/cm²; "
                        f"EW={result['equivalent_weight_g_equiv']} g/equivalent"
                    ),
                }

                add_experiment_record(record)
                st.success("Electrochemical result saved.")

    st.warning(
        "The result depends on the selected equivalent weight, dissolution "
        "valence, alloy composition, density, and current-density units. "
        "Verify the assumptions for your system before reporting results."
    )


# ---------------------------------------------------------
# INHIBITION EFFICIENCY
# ---------------------------------------------------------

elif page == "Inhibition Efficiency":

    page_header(
        "INHIBITOR PERFORMANCE",
        "Inhibition Efficiency",
        "Compare a blank corrosion rate with a corrosion rate measured in the presence of an inhibitor.",
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:

        with st.form("inhibition_form"):

            blank_rate = st.number_input(
                "Blank corrosion rate (mm/year)",
                min_value=0.0001,
                value=2.0,
                step=0.1,
                format="%.5f",
            )

            inhibited_rate = st.number_input(
                "Inhibited corrosion rate (mm/year)",
                min_value=0.0,
                value=0.5,
                step=0.1,
                format="%.5f",
            )

            inhibition_button = st.form_submit_button(
                "Calculate inhibition efficiency",
                type="primary",
                use_container_width=True,
            )

    with col2:

        st.subheader("Result")

        if inhibition_button:
            try:
                efficiency = calculate_inhibition_efficiency(
                    blank_rate,
                    inhibited_rate,
                )

                st.metric(
                    "Inhibition efficiency",
                    f"{efficiency:.2f}%",
                )

                st.latex(
                    r"IE(\%) = \frac{CR_{\mathrm{blank}}-CR_{\mathrm{inhibited}}}"
                    r"{CR_{\mathrm{blank}}}\times100"
                )

                if efficiency > 0:
                    st.success(
                        "The inhibited condition has a lower corrosion rate "
                        "than the blank condition."
                    )
                elif efficiency == 0:
                    st.info(
                        "The blank and inhibited corrosion rates are equal."
                    )
                else:
                    st.warning(
                        "The inhibited condition has a higher corrosion rate "
                        "than the blank. Check the data and experimental conditions."
                    )

            except (TypeError, ValueError) as error:
                st.error(str(error))

        else:
            st.info("Enter both corrosion rates and calculate.")

    st.caption(
        "Compare rates obtained using compatible methods, units, and exposure "
        "conditions. Inhibition efficiency can legitimately be negative."
    )


# ---------------------------------------------------------
# DATA & EXPERIMENTS
# ---------------------------------------------------------

elif page == "Data & Experiments":

    page_header(
        "RESEARCH RECORDS",
        "Data & Experiments",
        "Create, review, import, and export experimental records.",
    )

    with st.expander("Add a manual experiment record", expanded=False):

        with st.form("manual_record_form"):

            col1, col2, col3 = st.columns(3)

            experiment_id = col1.text_input(
                "Experiment ID",
                value=f"EXP-{len(st.session_state.experiments) + 1:04d}",
            )

            specimen = col2.text_input(
                "Specimen label",
                placeholder="e.g. MS-01",
            )

            medium = col3.text_input(
                "Test medium",
                placeholder="e.g. 1 M HCl",
            )

            col4, col5 = st.columns(2)

            initial = col4.number_input(
                "Initial mass (g)",
                min_value=0.0,
                value=10.0,
                step=0.001,
                format="%.4f",
            )

            final = col5.number_input(
                "Final mass (g)",
                min_value=0.0,
                value=9.8,
                step=0.001,
                format="%.4f",
            )

            notes = st.text_input(
                "Notes",
                placeholder="Temperature, concentration, replicate...",
            )

            manual_submit = st.form_submit_button(
                "Add record",
                type="primary",
            )

        if manual_submit:
            try:
                loss = calculate_mass_loss(initial, final)

                record = {
                    "recorded_on": date.today().isoformat(),
                    "experiment_id": experiment_id.strip()
                    or f"EXP-{len(st.session_state.experiments) + 1:04d}",
                    "method": "Manual record",
                    "specimen": specimen.strip() or "Not specified",
                    "medium": medium.strip() or "Not specified",
                    "initial_mass_g": initial,
                    "final_mass_g": final,
                    "mass_loss_g": loss,
                    "density_g_cm3": None,
                    "exposed_area_cm2": None,
                    "exposure_time_h": None,
                    "corrosion_rate_mm_year": None,
                    "notes": notes,
                }

                add_experiment_record(record)
                st.success("Experiment record added.")

            except (TypeError, ValueError) as error:
                st.error(str(error))

    st.subheader("Current session records")

    if not st.session_state.experiments:
        st.info(
            "No records yet. Save a calculation result or add a manual record."
        )

    else:
        df = pd.DataFrame(st.session_state.experiments)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Export experiment records as CSV",
            data=csv_data,
            file_name="corroscope_experiments.csv",
            mime="text/csv",
            type="primary",
        )

        with st.expander("Import records from CSV"):

            uploaded_file = st.file_uploader(
                "Choose a CSV file",
                type=["csv"],
                key="experiment_csv_upload",
            )

            if uploaded_file is not None:

                try:
                    imported_df = pd.read_csv(uploaded_file)

                    st.write("Preview:")
                    st.dataframe(
                        imported_df.head(10),
                        use_container_width=True,
                        hide_index=True,
                    )

                    if st.button("Append imported rows"):
                        imported_rows = (
                            imported_df.where(pd.notna(imported_df), None)
                            .to_dict(orient="records")
                        )

                        st.session_state.experiments.extend(imported_rows)
                        st.success(
                            f"Added {len(imported_rows)} row(s) to this session."
                        )
                        st.rerun()

                except Exception as error:
                    st.error(f"Could not read this CSV file: {error}")

        if st.button("Clear all session records"):
            st.session_state.experiments = []
            st.rerun()


# ---------------------------------------------------------
# LITERATURE NOTES
# ---------------------------------------------------------

elif page == "Literature Notes":

    page_header(
        "REFERENCE WORKSPACE",
        "Literature Notes",
        "Save and search your own reference notes by title, keyword, or finding.",
    )

    with st.form("literature_note_form"):

        note_title = st.text_input(
            "Reference title or citation",
            placeholder="Author, year, title...",
        )

        note_text = st.text_area(
            "Note or key finding",
            height=150,
            placeholder=(
                "Record the method, key result, limitations, or page number."
            ),
        )

        note_keywords = st.text_input(
            "Keywords, separated by commas",
            placeholder="mild steel, HCl, adsorption",
        )

        note_submit = st.form_submit_button(
            "Save literature note",
            type="primary",
        )

    if note_submit:

        if not note_title.strip() or not note_text.strip():
            st.warning("Enter both a reference title and a note.")

        else:
            st.session_state.literature_notes.append(
                {
                    "title": note_title.strip(),
                    "note": note_text.strip(),
                    "keywords": note_keywords.strip(),
                    "saved_on": date.today().isoformat(),
                }
            )

            st.success("Literature note saved for this session.")

    st.divider()

    search_query = st.text_input(
        "Search your saved notes",
        placeholder="Try: adsorption, HCl, inhibitor...",
    )

    notes = st.session_state.literature_notes

    matching_notes = [
        note
        for note in notes
        if not search_query.strip()
        or search_query.casefold()
        in (
            note["title"]
            + " "
            + note["note"]
            + " "
            + note["keywords"]
        ).casefold()
    ]

    if not matching_notes:
        st.info("No matching notes. Add a note or try another search term.")

    else:
        for note in matching_notes:
            with st.expander(
                f"{note['title']} · {note['saved_on']}"
            ):
                st.write(note["note"])

                if note["keywords"]:
                    st.caption(f"Keywords: {note['keywords']}")

    if notes:
        notes_csv = pd.DataFrame(notes).to_csv(index=False).encode("utf-8")

        st.download_button(
            "Export literature notes as CSV",
            data=notes_csv,
            file_name="corroscope_literature_notes.csv",
            mime="text/csv",
        )

    st.caption(
        "This section stores and searches notes you enter. It does not "
        "automatically search the internet or generate AI literature reviews."
    )


# ---------------------------------------------------------
# ABOUT & NAVIGATION
# ---------------------------------------------------------

elif page == "About & Navigation":

    page_header(
        "QUICK GUIDE",
        "About CorroScope",
        "What the application does and how to use it.",
    )

    st.subheader("What is CorroScope?")

    st.write(
        "CorroScope is a research companion for corrosion studies. "
        "It calculates selected corrosion metrics from measurements you "
        "provide and helps you organize experiment records and literature notes. "
        "It does not collect laboratory data automatically or replace your "
        "experimental protocol."
    )

    st.subheader("How to navigate")

    st.markdown(
        """
        - **Home:** view the workspace overview and shortcuts.
        - **Weight Loss Analysis:** enter initial and final masses, material
          density, exposed area, and exposure time to calculate mass loss
          and weight-loss corrosion rate.
        - **Electrochemical Analysis:** estimate corrosion rate from
          corrosion current density, equivalent weight, and density.
        - **Inhibition Efficiency:** compare blank and inhibitor corrosion
          rates to calculate percentage inhibition efficiency.
        - **Data & Experiments:** add records, review the session log, and
          import or export CSV files.
        - **Literature Notes:** save references and search your notes by
          keyword.
        """
    )

    st.subheader("Before using results in research")

    st.write(
        "Confirm units, material properties, equivalent weight assumptions, "
        "specimen preparation, and exposure conditions. Validate calculations "
        "against your laboratory protocol and relevant standards before using "
        "results in a thesis, report, or publication."
    )

    st.caption(
        "Records and notes are stored in the active session in this version. "
        "Export important data before ending the session."
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "CorroScope · Scientific research support. "
    "Verify formulas, units, and experimental assumptions before publication."
)
