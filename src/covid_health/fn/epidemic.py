def calculate_epidemic_age(
    df,
    group_col="sigla_provincia",
    time_col="data",
    total_cases_col="totale_casi",
    start_treshold=100,
):
    """Calculate epidemic age.
    
    `epidemic_age` is  defined as days diff from min day where 
    `total_cases >= start_treshold`.

    Parameters
    ----------

    df : DataFrame
        Source DataFrame.
    group_col : str
        Column containing the name/index of the group (ask yourself
        "for whom do I want to calculate the epidemic age?". There
        is yout answer to this parameter).
    time_col : str
        The column containing the date/datetime information.
    total_cases_col : str
        The column containing the total number of cases (or
        hospedalized or any other number to consider as number of
        cases benchmark).
    start_treshold : int
        The number of cases from which to assert the start of a
        "focolaio" (epicenter). Default is 100, aligned to the
        treshold considered by the Italian autorities.
    
    Returns
    -------
    DataFrame
        Same as before, but with `epidemic_start` and `epidemic_age`
        columns.

    """
    df["epidemic_start"] = (
        df.loc[df[total_cases_col] >= start_treshold]
        .groupby(group_col)
        [time_col].min()
        .dt.floor("D")
        .reindex(df[group_col].values)
        .values
    )

    df["epidemic_age"] = (df[time_col] - df["epidemic_start"]).dt.days

    return df
