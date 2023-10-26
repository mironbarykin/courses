import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        data = list()
        
        for row in reader:
            evidence = list()
            for i, cell in enumerate(row[:17]):
                if i in [0, 2, 4, 11, 12, 13, 14, 16]:
                    if cell == 'FALSE':
                        cell = False
                    elif cell == 'TRUE':
                        cell = True
                    evidence.append(int(cell))
                elif i == 10:
                    months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "June": 6, 
                              "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
                    evidence.append(months[cell])
                elif i == 15:
                    if cell == "Returning_Visitor":
                        evidence.append(1)
                    else:
                        evidence.append(0)
                else:
                    evidence.append(float(cell))
            
            data.append({
                "evidence": evidence,
                "label": 1 if row[-1] == 'TRUE' else 0
            })
    return [row["evidence"] for row in data], [row["label"] for row in data]

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    all_1, all_0, acc_1, acc_0 = labels.count(1), labels.count(0), 0, 0
    for i in range(len(predictions)):
        if predictions[i] == labels[i]:
            if predictions[i] == 1:
                acc_1 += 1
            else:
                acc_0 += 1    
    return acc_1 / all_1, acc_0 / all_0 
            
if __name__ == "__main__":
    main()

