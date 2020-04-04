__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Martindale, Nathan", "Smith, Steven",
               "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@students.tntech.edu"
__status__ = "Prototype"


# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import Machine_Learning.utils as utility

# Libraries relevant to performance metrics
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score
#from sklearn.model_selection import StratifiedKFold
#from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping


def mlp_model(X, Y):
    
    """ Generate a multilayer perceptron  model or ANN """
    
    # Initializing the ANN
    model = Sequential()
    
    # Adding the input layer and the first hidden layer
    model.add(Dense(output_dim = round(X.shape[1]/2), init =  'uniform', activation = 'relu', input_dim = X.shape[1]))
    
    # Adding the second hidden layer
    model.add(Dense(output_dim = round(X.shape[1]/2), init =  'uniform', activation = 'relu'))

    
    if(len(np.unique(Y)) > 2): # Multi-classification task
        # Adding the output layer
        model.add(Dense(output_dim = len(np.unique(Y)), init =  'uniform', activation = 'softmax'))
        # Compiling the ANN
        model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
    else: # Binary classification task
        # Adding the output layer
        model.add(Dense(output_dim = 1, init =  'uniform', activation = 'sigmoid'))
        # Compiling the ANN
        model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    
    print(model.summary())
    
    return model


def mlp_model_train(X, Y, val_split, batch_size, epochs_count):
    
    """ Train the multilayer perceptron  model or ANN """
    
    # Callback to stop if validation loss does not decrease
    callbacks = [EarlyStopping(monitor='val_loss', patience=2)]

    # Fitting the ANN to the Training set
    history = model.fit(X, Y,
                   callbacks=callbacks,
                   validation_split=val_split,
                   batch_size = batch_size,
                   epochs = epochs_count,
                   shuffle=True)

    print(history.history)
    print(model.summary())
    return history


def mlp_model_eval(X, Y, model, history, ransomware_hash):
    
    """ Evaluate the multilayer perceptron  model or ANN during test time """
    
    # Predicting the results given instances X
    Y_pred = model.predict_classes(X)
    Y_pred = (Y_pred > 0.5)

    # Breakdown of statistical measure based on classes
    print(classification_report(Y, Y_pred, digits=4))

    # Making the cufusion Matrix
    cm = confusion_matrix(Y, Y_pred)
    print("Confusion Matrix:\n", cm)
    print("Accuracy: ", accuracy_score(Y, Y_pred))

    if(len(np.unique(Y))) == 2:
        print("F1: ", f1_score(Y, Y_pred, average='binary'))
        print("Precison: ", precision_score(Y, Y_pred, average='binary'))
        print("Recall: ", recall_score(Y, Y_pred, average='binary'))
    else:
        f1_scores = f1_score(Y, Y_pred, average=None)
        print("F1: ", np.mean(f1_scores))
        precision_scores = precision_score(Y, Y_pred, average=None)
        print("Precison: ", np.mean(precision_scores))
        recall_scores = recall_score(Y, Y_pred, average=None)
        print("Recall: ", np.mean(recall_scores))

    # ------------ Print Accuracy over Epoch --------------------

    # Intilization of the figure
    myFig = plt.figure(figsize=[12,10])

    plt.plot(history.history['acc'], linestyle = ':',lw = 2, alpha=0.8, color = 'black')
    plt.plot(history.history['val_acc'], linestyle = '--',lw = 2, alpha=0.8, color = 'black')
    plt.title('Accuracy over Epoch', fontsize=20, weight='bold')
    plt.ylabel('Accuracy', fontsize=18, weight='bold')
    plt.xlabel('Epoch', fontsize=18, weight='bold')
    plt.legend(['Train', 'Validation'], loc='lower right', fontsize=14)
    plt.xticks(ticks=range(0, len(history.history['acc'])))
    
    plt.yticks(fontsize=16)
    plt.show()
        
    if(len(np.unique(Y))) == 2:
        fileName = str(ransomware_hash) + '_ANN_Accuracy_over_Epoch_Binary_Classification.eps'
    else:
        fileName = str(ransomware_hash) + '_ANN_Accuracy_over_Epoch_Multiclass_Classification.eps'
    
    # Saving the figure
    myFig.savefig(fileName, format='eps', dpi=1200)
    
    # ------------ Print Loss over Epoch --------------------

    # Clear figure
    plt.clf()
    myFig = plt.figure(figsize=[12,10])
    
    plt.plot(history.history['loss'], linestyle = ':',lw = 2, alpha=0.8, color = 'black')
    plt.plot(history.history['val_loss'], linestyle = '--',lw = 2, alpha=0.8, color = 'black')
    plt.title('Loss over Epoch', fontsize=20, weight='bold')
    plt.ylabel('Loss', fontsize=18, weight='bold')
    plt.xlabel('Epoch', fontsize=18, weight='bold')
    plt.legend(['Train', 'Validation'], loc='upper right', fontsize=14)
    plt.xticks(ticks=range(0, len(history.history['loss'])))
    
    plt.yticks(fontsize=16)
    plt.show()
        
    if(len(np.unique(Y))) == 2:
        fileName = str(ransomware_hash) + '_ANN_Loss_over_Epoch_Binary_Classification.eps'
    else:
        fileName = str(ransomware_hash) + '_ANN_Loss_over_Epoch_Multiclass_Classification.eps'
    
    # Saving the figure
    myFig.savefig(fileName, format='eps', dpi=1200)
    
    
    # ------------ ROC Curve --------------------

    # Clear figure
    plt.clf()
    myFig = plt.figure(figsize=[12,10])
    
    if len(np.unique(Y)) == 2:
        fpr, tpr, _ = roc_curve(Y_test, Y_pred)
        plt.plot(fpr, tpr, color='black',
                label=r'ROC (AUC = %0.3f)' % (auc(fpr, tpr)),
                lw=2, alpha=0.8)
            
        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])
        plt.xlabel('False Positive Rate', fontsize=18, weight='bold')
        plt.ylabel('True Positive Rate', fontsize=18, weight='bold')
        plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=20, fontweight='bold')
        plt.legend(loc="lower right",fontsize=14)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.show()
        
        fileName = str(ransomware_hash) + '_ANN_Binary_Classification_ROC.eps'

        # Saving the figure
        myFig.savefig(fileName, format='eps', dpi=1200)
        

if __name__ == '__main__':
    
    # Get rasomware files
    all_ransomware_files = utility.getRansomwareFiles()
    ransomware_file = all_ransomware_files[0]
    
    # First splitting from the f
    ransomware_hash = ransomware_file.split('/')[-1].split('_')[0]
    
    # Get processed dataset (X and Y) for the ransomware dataset
    X, Y_class, Y_family = utility.getProcessedDataset(ransomware_file)
    
    # Split the dataset into train set (80%) and test set (20%)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y_class, test_size = 0.2, random_state = 42, stratify=Y_class)
    
    # Building the model
    model = mlp_model(X_train, Y_train)
    
    # Training the model
    history = mlp_model_train(X_train, Y_train,
                0.1, # Validation Split
                64, # Batch Size
                100 # Epoch Count
                )
    
    # Evaluation of the model
    mlp_model_eval(X_test, Y_test, model, history, ransomware_hash)