from sklearn import metrics
from imblearn.combine import SMOTEENN
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import ParameterGrid


# create models with grid search
# from sklearn.grid_search import ParameterGrid
def grid_search_generator(classifier, param_grid={}):
    # define model
    for params in ParameterGrid(param_grid):
        mdl = classifier(**params)
        print("model configuration:")
        print(params)
        yield mdl


# cross-validation
# from sklearn import metrics
# from sklearn.model_selection import StratifiedShuffleSplit
def eval_model_cv(classifier, X, y, k=10, eval_metric='auc', params={}):
    sss = StratifiedShuffleSplit(n_splits=k, random_state=40)
    score_metrics = ['accuracy', 'roc_auc', 'precision', 'recall']
    # iterate over all possible models
    for model in grid_search_generator(classifier, params):
        # total scores for all score metrics
        train_result = [0 for s in score_metrics]
        test_result = [0 for s in score_metrics]
        for train_index, test_index in sss.split(X, y):
            # prepare data
            X_train_cv, X_test_cv = X[train_index], X[test_index]
            y_train_cv, y_test_cv = y[train_index], y[test_index]
            # apply SMOTE + ENN on train data
            print('Datasize: ', end='')  # noqa
            sm = SMOTEENN()
            X_train_rs, y_train_rs = sm.fit_sample(X_train_cv, y_train_cv)
            print(X_train_rs.shape)

            # train the model
            model.fit(X_train_rs, y_train_rs, eval_metric='auc')

            # evaluate the model
            # check on train
            print('TRAIN: ', end='')
            y_true = y_train_cv
            y_pred = model.predict(X_train_cv)
            y_prob = model.predict_proba(X_train_cv)[:, 1]
            for i, metric in enumerate(score_metrics):
                function = getattr(metrics, metric + '_score')
                if 'roc' in metric:
                    score = function(y_true, y_prob)
                else:
                    score = function(y_true, y_pred)
                train_result[i] += score
                print('  ' + metric + ': ', end='')
                print('%.4g' % score, end='')
            print()

            # check on test
            print('TEST: ', end='')
            y_true = y_test_cv
            y_pred = model.predict(X_test_cv)
            y_prob = model.predict_proba(X_test_cv)[:, 1]
            # calculating metric using different result
            for i, metric in enumerate(score_metrics):
                function = getattr(metrics, metric + '_score')
                if 'roc' in metric:
                    score = function(y_true, y_prob)
                else:
                    score = function(y_true, y_pred)
                test_result[i] += score
                print('  ' + metric + ': ', end='')
                print('%.4g' % score, end='')
            print()

        # summary the model
        print("\nModel Report")
        for i, metric in enumerate(score_metrics):
            print("TRAIN: average " + metric + " : %.4g" % (train_result[i]/k))
        for i, metric in enumerate(score_metrics):
            print("TEST: average " + metric + " : %.4g" % (test_result[i]/k))
        print()
