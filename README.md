# pat_classifier

Python package to classify patents into process and product based on titles and claims

## Change log v20230126:
- changed to a pure python implementation rather than spark
- Expand the transitional phrase / Update the parsing logic for the procedure to obtain preamble for claims, keywords for titles
- Added new words to process list like manner, preparing, cleaning, removing, connecting, activity, removed combination
- System must be coupled with a leading word to be a product such as computer system, optical system, otherwise process. e.g. System and method would still be a process
- Added manually crated test data to gauge performance (94% accuracy)
