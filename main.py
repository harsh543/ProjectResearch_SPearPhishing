import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD 
from sklearn.preprocessing import normalize 
def top_tfidf_features(row,features,top_n=20):
    topn_ids=np.argsort(row)[::-1][:top_n]
    top_feats=[(features[i],row[i]) for i in topn_ids]
    df=pd.DataFrame(top_feats,columns=['features','score'])
    return df

def top_features_in_doc(X,features,row_id,top_n=25):
    row=np.squeeze(X[row_id].toarray())
    return top_tfidf_features(row,features,top_n)

def top_mean_features(X,features,grp_ids=None,min_tfidf=0.1,top_n=25):
    if grp_ids:
        D=X[grp_ids].toarray()
    else:
        D=X.toarray()

    D[D < min_tfidf] =0 
    tfidf_means=np.mean(D,axis=0)
    return top_tfidf_features(tfidf_means,features,top_n)

def top_features_per_cluster(X,y,features,min_tfidf=0.1,top_n=25):
    labels=np.unique(y)
    dfs=[]
    for label in labels:
        ids=np.where(y==label)
        features_df = top_mean_features(X,features,ids,min_tfidf=min_tfidf,top_n=top_n)
        features_df.label=label
        dfs.append(features_df)
    return dfs    


def plot_tfidf_classfeatures_h(dfs):
    fig=plt.figure(figsize=(12,9),facecolor="w")
    x=np.arange(len(dfs[0]))
    for i, df in enumerate(dfs):
        ax= fig.add_subplot(1,len(dfs),i+1)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.set_frame_on(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_xlabel("Tfidf score",labelpad=16,fontsize=14)
        ax.set_title("Cluster labels ="+str(df.label),fontsize=16)
        ax.ticklabel_format(axis='x',style='sci',scilimits=(-2,2))
        ax.barh(x,df.score,align='center',color='#7530FF')
        ax.set_yticks(x)
        ax.set_ylim([-1,x[-1]+1])
        yticks=ax.set_yticklabels(df.features)
        plt.subplots_adjust(bottom=0.09,right=0.97,left=0.15,top=0.95,wspace=0.52)
    plt.show()    
