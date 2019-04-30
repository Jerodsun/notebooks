"""
https://www.fjc.gov/history/judges/biographical-directory-article-iii-federal-judges-export

Code for jupyter notebook "Education of Federal Judges"

Jerod

4/30/2019 Update

"""

import pandas as pd

df = pd.read_csv("education.csv")
df2 = pd.read_csv("judges.csv")

df["Degree Year"] = pd.to_numeric(df["Degree Year"], errors = "coerce")

df.set_index("nid", inplace = True, drop = False)
df2.set_index("nid", inplace = True, drop = False)


def name_correction(dataframe):
    """These are common repeats. Columbia MAY refer to a different school, 
    but anecdotally, I only found one. """
    
    dataframe = dataframe.replace(["Harvard College", "Radcliffe College", "Yale College", 
                                   "Georgetown University School of Foreign Service", "Columbia College", 
                                   "Louisiana State University, Paul M. Hebert Law Center"], 
                                  ["Harvard University", "Harvard University", "Yale University", 
                                   "Georgetown University", "Columbia University", 
                                   "Louisiana State University Law School"])
    
    return dataframe

def by_president(presidents = ["Barack Obama", "Donald J. Trump"]):
    """ List the full name of the appointing presidents as listed in the csv. Returns a dataframe
    of the appointees with Index(['nid', 'Sequence', 'Judge Name', 'School', 'Degree', 'Degree Year',
       'Court Name']"""
    
    if type(presidents) != list: # single name
        presidents = [presidents]
        
        
    nominees_id = df2[df2["Appointing President (1)"].isin(presidents)]["nid"]
    education = df[df["nid"].isin(nominees_id)]
    education = name_correction(education)

    court = df2[df2["Appointing President (1)"].isin(presidents)]["Court Name (1)"]

    education["Court Name"] = court
    
    return education



def degree_parse(dataframe, degree = "UG", include_LLB = True):
    """Specify degree: UG or Law. LLB degrees in lieu of JD are frequent up to the Clinton appointee era.""" 
    if degree not in ["UG", "Law"]: raise NotImplementedError

    undergrad = dataframe[dataframe["Sequence"] == 1]

    if include_LLB:
        law = dataframe[dataframe["Degree"].isin(["J.D.", "LL.B."])]
    else:
        law = dataframe[dataframe["Degree"] == "J.D."]
        
    if len(law) != len(undergrad):
        print("UserWarning: law school number: " + str(len(law))
        + " undergrad institution: " + str(len(undergrad))
        + """\nUndergrad Institution relies on degree sequence, which may be
        inaccurate. Law is parsed by J.D., while older law degrees may be LL.B.""")
    
    return undergrad if (degree == "UG") else law


def count(dataframe):
    return dataframe["School"].value_counts()



def inclusive_or(dataframe):
    return (dataframe["In District"] | dataframe["T14 Law School"]).sum()/len(dataframe)


if __name__ == "__main__":
    presidents = ["Barack Obama", "William J. Clinton", "George W. Bush", "Donald J. Trump"]
    
    all_t14 = ["Harvard Law School", "Yale Law School", "Stanford Law School", "University of California, Berkeley, Boalt Hall School of Law", "University of Pennsylvania Law School", "Georgetown University Law Center", "New York University School of Law", "University of Texas School of Law", "University of Virginia School of Law", "Columbia Law School", "University of Michigan Law School", "Northwestern University School of Law", "Duke University School of Law", "University of Chicago Law School", "Cornell Law School"]
    judges = by_president(presidents)
    judges = degree_parse(judges, degree = "Law")
    law_schools = count(judges)
