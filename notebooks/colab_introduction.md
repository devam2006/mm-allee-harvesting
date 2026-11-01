# Mathematical Modelling of Population Harvesting under a Strong Allee Effect: Equilibria, Stability, Extinction and PINN Analysis

## Project Overview

In this project, we study how harvesting affects a population that follows the strong Allee effect. This means that if the population falls below a certain minimum size, it may continue to decline even without further harvesting.

We use fishing as an example of harvesting, where the term *stock* refers to the population being studied, measured either by the number of individuals or by their total weight. *Catch* refers to the amount removed from the population per unit time.

We consider two harvesting methods:

- **Constant harvesting (Model A):** A fixed amount $H$ is removed per unit time, regardless of the current population size.
- **Proportional harvesting (Model B):** The amount removed is $hN$, where $N$ is the current population and $h$ is the harvesting-rate coefficient, also called fishing effort. Thus, the catch decreases as the population becomes smaller.

For example, if the population is 100 units, a constant harvest of 10 units per time unit remains unchanged even if the population decreases to 50. However, with proportional harvesting at $h=0.1$ per time unit, the catch decreases from 10 to 5 units per time unit.

We study the equilibrium points, stability, collapse thresholds, and extinction behaviour of these models. We then use Physics-Informed Neural Networks (PINNs) to solve the equations and estimate unknown parameters from simulated observations. All data used in this project are synthetic.

## Contributors

| Section | Names                | ID            |
| ------------ | -------------------- | ------------- |
| 1         | Raghav Singhal       | 2024ADPS0827G |
| 2         | Ashwath Chandramouli | 2024ADPS0853G |
| 3         | Devam Jatin Bhavsar  | 2024ADPS0831G |
| 4         | Mehta Prem Kalpesh   | 2024ADPS0851G |
| 5         | Rohan Agrawal        | 2024ADPS0004G |

**Running this notebook:** Open the notebook in Google Colab, connect to a CPU runtime, and select **Runtime → Run all**. The notebook automatically downloads the necessary Python code and synthetic data, runs the experiments, and displays the corresponding calculations, tables, and graphs. An internet connection is required for the initial setup, but no Google Drive connection or API key is needed. The source code, experimental data, and supporting documentation can be found in our [GitHub project repository](https://github.com/devam2006/mm-allee-harvesting).&#x20;
