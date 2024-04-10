# cTool: A Comprehensive Decision Analysis Tool

cTool is a powerful decision analysis tool designed to facilitate stakeholder decision-making in complex systems. It provides a comprehensive interface for stakeholders to explore alternative decisions and understand their impact on the system's goals.

## Features

### Input Interface
cTool generates a unique form for each stakeholder, containing all Jucmnav tasks. Tasks that are certain or already completed are pre-filled to 100%, while the rest, which we refer to as cTool inputs, represent decisions with associated uncertainty.

### Output Generation
Upon receiving stakeholder inputs, cTool calls Jucmnav in the background and generates a detailed report for each stakeholder goal. The report contains two types of results:

1. **Independent Results**: These are results that are satisfied, not satisfied, or partially satisfied, independent of other stakeholders' decisions.
2. **Dependent Results**: These are results whose satisfaction level depends on other stakeholders' choices.

To determine which result type applies to each goal, cTool generates best-worst case scenarios and performs a differential analysis. If the analysis shows no difference, the result is of type (a). Otherwise, it is of type (b).

### Result Analysis
cTool provides a robust analysis of the results. If all the goals in the output are of type (a), the stakeholder can analyze the impact of their own decisions. If many goals are of type (b), the stakeholder can infer that the system is immature or that significant interaction is needed with other stakeholders. This serves as a metric of stability from the user's perspective and a metric of understanding user requirements from the developer's perspective. If only a few goals are of type (b), stakeholders can still understand the impact of some of their decisions that are stable.

## Conclusion
cTool is a comprehensive tool that aids stakeholders in making informed decisions by providing a clear understanding of the impact of their choices on the system's goals. It is an invaluable resource for any complex system where multiple stakeholders' decisions interact and influence the system's outcomes.


<img src="https://i.ibb.co/rc6mjPr/c-Tool-drawio-1.png" width="250" height="250">
