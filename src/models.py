""" Module for setting up statistical models
"""

import pylab as pl
import pymc as mc

import data

def linear():
    beta = mc.Uninformative('beta', value=[0., 0.])
    sigma = mc.Uninformative('sigma', value=1.)

    @mc.deterministic
    def y_pred(beta=beta, X=data.hdi):
        return beta[0] + beta[1]*X
    y_obs = mc.Normal('y_obs', value=data.tfr,
                      mu=y_pred, tau=sigma**-2,
                      observed=True)

    return vars()

def fit_linear():
    vars = linear()

    mc.MAP(vars).fit(method='fmin_powell')

    m = mc.MCMC(vars)
    m.sample(iter=10000, burn=5000, thin=5)
    return m

def nonlinear():
    beta = mc.Uninformative('beta', value=[0., 0., 0.])
    gamma = mc.Normal('gamma', mu=.86, tau=.05**-2, value=.86)
    sigma = mc.Uninformative('sigma', value=1.)

    @mc.deterministic
    def y_pred(beta=beta, gamma=gamma, X=data.hdi):
        return beta[0] + beta[1]*X \
            + pl.maximum(0., beta[2]*(X-gamma))
    y_obs = mc.Normal('y_obs', value=data.tfr,
                      mu=y_pred, tau=sigma**-2,
                      observed=True)

    return vars()

def fit(vars):
    mc.MAP(vars).fit(method='fmin_powell')

    m = mc.MCMC(vars)
    m.sample(iter=10000, burn=5000, thin=5)
    return m

if __name__ == '__main__':
    reload(data)
    ml = fit_linear()
    mn = fit(nonlinear())

    import graphics
    reload(graphics)
    reload(graphics.data)

    pl.clf()

    graphics.plot_all_data()
    graphics.plot_linear_model(ml)
    graphics.plot_nonlinear_model(mn)

    pl.show()
