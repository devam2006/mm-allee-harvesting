
MATHEMATICAL MODELLING PROJECT
BITS Pilani, K. K. Birla Goa Campus

Title:
Mathematical Modelling of Population Harvesting under a
Strong Allee Effect: Equilibria, Stability, Extinction
and PINN Analysis


ABOUT THE PROJECT

This project studies population growth under a strong
Allee effect with two harvesting models:

Model A - Constant harvesting
Model B - Proportional harvesting

The report covers equilibrium analysis, stability,
critical harvesting rates, extinction, numerical
simulations, and forward and inverse Physics-Informed
Neural Networks (PINNs).

All numerical data used in the project are synthetic.


REPORT STRUCTURE

main.tex
    Main LaTeX file. Compile this to generate the report.

preamble.tex
    LaTeX packages and document formatting.

abstract.tex
    Project abstract.

frontmatter.tex
    Introduction, motivation, assumptions and models.

sections/
    01_foundations.tex
        Mathematical foundations and Model A.

    02_model_b_history.tex
        Model B and harvesting comparisons.

    03_collapse.tex
        Critical harvesting rates, extinction times
        and numerical verification.

    04_forward_pinn.tex
        Forward PINN analysis.

    05_inverse_validation.tex
        Inverse PINNs and parameter estimation.

    conclusions.tex
        Main findings and limitations.

    acknowledgements.tex
        Contributions, sources and AI acknowledgements.

figures/
    Figures used in the report, all in EPS format.

references.bib
    Bibliography and citations.


HOW TO COMPILE

In Overleaf:
1. Set main.tex as the main document.
2. Select pdfLaTeX as the compiler.
3. Click Recompile.

For local compilation, use a complete LaTeX installation
with BibTeX and EPS conversion support. Compile main.tex.

The original EPS figures are included. Separate
preconverted figure PDFs are not required.


SOURCE CODE AND NOTEBOOK

Project repository:
https://github.com/devam2006/mm-allee-harvesting

Runnable Jupyter notebook:
https://colab.research.google.com/drive/1uOFkJ9w4_R_EVSaynWwtOavZEufCAhyT#scrollTo=wp05-cell-010

The repositories contain the Python implementations,
experiment configurations, synthetic data generation
and numerical results.

The report PDF and accompanying notebook are provided
separately as part of the project submission.
