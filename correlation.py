# Merge translation results from different inference models and evaluation metrics, 
# and calculate Pearson's R correlation between dictionary accuracy and human evaluation.
# Keara Berlin 24 April 2023

import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from helpers import GOOGLE, M2M, CHATGPT

input_paths = {
    GOOGLE: f'output/{GOOGLE}_dict_acc.csv',
    M2M: f'output/{M2M}_dict_acc.csv',
    CHATGPT: f'output/{CHATGPT}_dict_acc.csv'
}

def get_col_map(name):
    return {"Chinese": f"Chinese_{name}",
            "Terms": f"Terms_{name}",
            "Correct Terms": f"Correct_Terms_{name}", 
            "Dictionary Accuracy": f"Dict_Acc_{name}"}

def get_df(name, nickname):
    df = pd.read_csv(input_paths[name])
    # df = df[['English', 'Chinese', 'Dictionary Accuracy']]
    df = df.rename(columns=get_col_map(nickname))
    return df

def get_eval_df(filepath, name, include_med_term_acc):
    df = pd.read_csv(filepath)
    if include_med_term_acc:
        df = df[['English', 'Human Evaluation Score (Out of 10)', 'Human eval on medical term accuracy(out of 5)']]
        df = df.rename(columns={'Human Evaluation Score (Out of 10)': f'Human Eval {name}',
                                'Human eval on medical term accuracy(out of 5)': f'Human Eval Medical {name}'})
    else:
        df = df[['English', 'Human Evaluation Score (Out of 10)']]
        df = df.rename(columns={'Human Evaluation Score (Out of 10)': f'Human Eval {name}'})
    return df

google_df = get_df(GOOGLE, "Google")
m2m_df = get_df(M2M, "M2M")
gpt_df = get_df(CHATGPT, "GPT")

google_eval = get_eval_df('evals/google_translations_evaluation.csv', "Google", False)
m2m_eval = get_eval_df('evals/m2m100_translations_evaluation.csv', "M2M", True)
gpt_eval = get_eval_df('evals/gpt_translations_evaluation.csv', "GPT", False)

def merge(df1, df2):
    return df1.merge(df2, how="inner", left_on=['English'], right_on=['English'])

df = merge(google_df, m2m_df)
df = merge(df, gpt_df)

df = merge(df, google_eval)
df = merge(df, m2m_eval)
df = merge(df, gpt_eval)

def plot_pearson(col1, col2, name, aspect, ymax=10.5):
    df_no_nan = df[df[col1].notna()]
    df_no_nan = df_no_nan[df_no_nan[col2].notna()]
    pearson = pearsonr(df_no_nan[col1], df_no_nan[col2])

    plt.rcParams.update({'font.size': 14})

    plt.scatter(df_no_nan[col1], df_no_nan[col2], s=225)
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.ylim((0,ymax))
    plt.title(f"{name} {aspect} R={pearson.statistic:0.4f} p={pearson.pvalue:0.4f}")
    plt.savefig(f'plots/{col1}_vs_{col2}.png', dpi=600)
    plt.show()
    plt.close()

plot_pearson('Dict_Acc_Google', 'Human Eval Google', "Google", 'Fluency/Terms')
plot_pearson('Dict_Acc_M2M', 'Human Eval M2M', "M2M", 'Fluency')
plot_pearson('Dict_Acc_M2M', 'Human Eval Medical M2M', 'M2M', 'Terms', ymax=5.3)
plot_pearson('Dict_Acc_GPT', 'Human Eval GPT', 'GPT', 'Fluency/Terms')
# plot_pearson('Dict_Acc_GPT', 'Human Eval Medical GPT', 'GPT', 'Terms', ymax=5.3)
