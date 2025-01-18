#!/bin/env python
"""

Wrapper for emcee

"""

import numpy as np
from .minimizer import _nan_policy

# check for emcee
try:
    import emcee
    from emcee.autocorr import AutocorrError
    HAS_EMCEE = int(emcee.__version__[0]) >= 3
except ImportError:
    HAS_EMCEE = False

# check for pandas
try:
    import pandas as pd
    from pandas import isnull
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    isnull = np.isnan

def _lnprob(minimizer, theta, userfcn, params, var_names, bounds, userargs=(),
            userkws=None, float_behavior='posterior', is_weighted=True,
            nan_policy='raise'):
    """Calculate the log-posterior probability.

    See the `Minimizer.emcee` method for more details.

    Parameters
    ----------
    minimizer : minimizer
        Minimizer instance
    theta : sequence
        Float parameter values (only those being varied).
    userfcn : callable
        User objective function.
    params : Parameters
        The entire set of Parameters.
    var_names : list
        The names of the parameters that are varying.
    bounds : numpy.ndarray
        Lower and upper bounds of parameters, with shape
        ``(nvarys, 2)``.
    userargs : tuple, optional
        Extra positional arguments required for user objective function.
    userkws : dict, optional
        Extra keyword arguments required for user objective function.
    float_behavior : {'posterior', 'chi2'}, optional
        Specifies meaning of objective when it returns a float. Use
        `'posterior'` if objective function returns a log-posterior
        probability (default) or `'chi2'` if it returns a chi2 value.
    is_weighted : bool, optional
        If `userfcn` returns a vector of residuals then `is_weighted`
        (default is True) specifies if the residuals have been weighted
        by data uncertainties.
    nan_policy : {'raise', 'propagate', 'omit'}, optional
        Specifies action if `userfcn` returns NaN values. Use `'raise'`
        (default) to raise a `ValueError`, `'propagate'` to use values
        as-is, or `'omit'` to filter out the non-finite values.

    Returns
    -------
    lnprob : float
        Log posterior probability.

    """
    # the comparison has to be done on theta and bounds. DO NOT inject theta
    # values into Parameters, then compare Parameters values to the bounds.
    # Parameters values are clipped to stay within bounds.
    if np.any(theta > bounds[:, 1]) or np.any(theta < bounds[:, 0]):
        return -np.inf
    for name, val in zip(var_names, theta):
        params[name].value = val
    userkwargs = {}
    if userkws is not None:
        userkwargs = userkws
    # update the constraints
    params.update_constraints()
    # now calculate the log-likelihood
    out = userfcn(params, *userargs, **userkwargs)
    minimizer.result.nfev += 1
    if callable(minimizer.iter_cb):
        abort = minimizer.iter_cb(params, minimizer.result.nfev, out,
                             *userargs, **userkwargs)
        minimizer._abort = minimizer._abort or abort
    if minimizer._abort:
        minimizer.result.residual = out
        minimizer._lastpos = theta
        raise AbortFitException("fit aborted by user.")
    else:
        out = _nan_policy(np.asarray(out).ravel(),
                          nan_policy=minimizer.nan_policy)
    lnprob = np.asarray(out).ravel()
    if len(lnprob) == 0:
        lnprob = np.array([-1.e100])
    if lnprob.size > 1:
        # objective function returns a vector of residuals
        if '__lnsigma' in params and not is_weighted:
            # marginalise over a constant data uncertainty
            __lnsigma = params['__lnsigma'].value
            c = np.log(2 * np.pi) + 2 * __lnsigma
            lnprob = -0.5 * np.sum((lnprob / np.exp(__lnsigma)) ** 2 + c)
        else:
            lnprob = -0.5 * (lnprob * lnprob).sum()
    else:
        # objective function returns a single value.
        # use float_behaviour to figure out if the value is posterior or chi2
        if float_behavior == 'posterior':
            pass
        elif float_behavior == 'chi2':
            lnprob *= -0.5
        else:
            raise ValueError("float_behaviour must be either 'posterior' "
                             "or 'chi2' " + float_behavior)
    return lnprob

def emcee(minimizer, params=None, steps=1000, nwalkers=100, burn=0, thin=1,
          ntemps=1, pos=None, reuse_sampler=False, workers=1,
          float_behavior='posterior', is_weighted=True, seed=None,
          progress=True, run_mcmc_kwargs={}):
    r"""Bayesian sampling of the posterior distribution.

    The method uses the ``emcee`` Markov Chain Monte Carlo package and
    assumes that the prior is Uniform. You need to have ``emcee``
    version 3 or newer installed to use this method.

    Parameters
    ----------
    minimizer : minimizer
        Minimizer instance
    params : Parameters, optional
        Parameters to use as starting point. If this is not specified
        then the Parameters used to initialize the Minimizer object
        are used.
    steps : int, optional
        How many samples you would like to draw from the posterior
        distribution for each of the walkers?
    nwalkers : int, optional
        Should be set so :math:`nwalkers >> nvarys`, where ``nvarys``
        are the number of parameters being varied during the fit.
        'Walkers are the members of the ensemble. They are almost like
        separate Metropolis-Hastings chains but, of course, the proposal
        distribution for a given walker depends on the positions of all
        the other walkers in the ensemble.' - from the `emcee` webpage.
    burn : int, optional
        Discard this many samples from the start of the sampling regime.
    thin : int, optional
        Only accept 1 in every `thin` samples.
    ntemps : int, deprecated
        ntemps has no effect.
    pos : numpy.ndarray, optional
        Specify the initial positions for the sampler, an ndarray of
        shape ``(nwalkers, nvarys)``. You can also initialise using a
        previous chain of the same `nwalkers` and ``nvarys``. Note that
        ``nvarys`` may be one larger than you expect it to be if your
        ``userfcn`` returns an array and ``is_weighted=False``.
    reuse_sampler : bool, optional
        Set to True if you have already run `emcee` with the
        `Minimizer` instance and want to continue to draw from its
        ``sampler`` (and so retain the chain history). If False, a
        new sampler is created. The keywords `nwalkers`, `pos`, and
        `params` will be ignored when this is set, as they will be set
        by the existing sampler.
        **Important**: the Parameters used to create the sampler must
        not change in-between calls to `emcee`. Alteration of Parameters
        would include changed ``min``, ``max``, ``vary`` and ``expr``
        attributes. This may happen, for example, if you use an altered
        Parameters object and call the `minimize` method in-between
        calls to `emcee`.
    workers : Pool-like or int, optional
        For parallelization of sampling. It can be any Pool-like object
        with a map method that follows the same calling sequence as the
        built-in `map` function. If int is given as the argument, then
        a multiprocessing-based pool is spawned internally with the
        corresponding number of parallel processes. 'mpi4py'-based
        parallelization and 'joblib'-based parallelization pools can
        also be used here. **Note**: because of multiprocessing
        overhead it may only be worth parallelising if the objective
        function is expensive to calculate, or if there are a large
        number of objective evaluations per step
        (``nwalkers * nvarys``).
    float_behavior : str, optional
        Meaning of float (scalar) output of objective function. Use
        `'posterior'` if it returns a log-posterior probability or
        `'chi2'` if it returns :math:`\chi^2`. See Notes for further
        details.
    is_weighted : bool, optional
        Has your objective function been weighted by measurement
        uncertainties? If ``is_weighted=True`` then your objective
        function is assumed to return residuals that have been divided
        by the true measurement uncertainty ``(data - model) / sigma``.
        If ``is_weighted=False`` then the objective function is
        assumed to return unweighted residuals, ``data - model``. In
        this case `emcee` will employ a positive measurement
        uncertainty during the sampling. This measurement uncertainty
        will be present in the output params and output chain with the
        name ``__lnsigma``. A side effect of this is that you cannot
        use this parameter name yourself.
        **Important**: this parameter only has any effect if your
        objective function returns an array. If your objective function
        returns a float, then this parameter is ignored. See Notes for
        more details.
    seed : int or numpy.random.RandomState, optional
        If `seed` is an ``int``, a new `numpy.random.RandomState`
        instance is used, seeded with `seed`.
        If `seed` is already a `numpy.random.RandomState` instance,
        then that `numpy.random.RandomState` instance is used. Specify
        `seed` for repeatable minimizations.
    progress : bool, optional
        Print a progress bar to the console while running.
    run_mcmc_kwargs : dict, optional
        Additional (optional) keyword arguments that are passed to
        ``emcee.EnsembleSampler.run_mcmc``.

    Returns
    -------
    MinimizerResult
        MinimizerResult object containing updated params, statistics,
        etc. The updated params represent the median of the samples,
        while the uncertainties are half the difference of the 15.87
        and 84.13 percentiles. The `MinimizerResult` contains a few
        additional attributes: `chain` contain the samples and has
        shape ``((steps - burn) // thin, nwalkers, nvarys)``.
        `flatchain` is a `pandas.DataFrame` of the flattened chain,
        that can be accessed with `result.flatchain[parname]`.
        `lnprob` contains the log probability for each sample in
        `chain`. The sample with the highest probability corresponds
        to the maximum likelihood estimate. `acor` is an array
        containing the auto-correlation time for each parameter if the
        auto-correlation time can be computed from the chain. Finally,
        `acceptance_fraction` (an array of the fraction of steps
        accepted for each walker).

    Notes
    -----
    This method samples the posterior distribution of the parameters
    using Markov Chain Monte Carlo. It calculates the log-posterior
    probability of the model parameters, `F`, given the data, `D`,
    :math:`\ln p(F_{true} | D)`. This 'posterior probability' is
    given by:

    .. math::

        \ln p(F_{true} | D) \propto \ln p(D | F_{true}) + \ln p(F_{true})

    where :math:`\ln p(D | F_{true})` is the 'log-likelihood' and
    :math:`\ln p(F_{true})` is the 'log-prior'. The default log-prior
    encodes prior information known about the model that the log-prior
    probability is ``-numpy.inf`` (impossible) if any of the parameters
    is outside its limits, and is zero if all the parameters are inside
    their bounds (uniform prior). The log-likelihood function is [1]_:

    .. math::

        \ln p(D|F_{true}) = -\frac{1}{2}\sum_n \left[\frac{(g_n(F_{true}) - D_n)^2}{s_n^2}+\ln (2\pi s_n^2)\right]

    The first term represents the residual (:math:`g` being the
    generative model, :math:`D_n` the data and :math:`s_n` the
    measurement uncertainty). This gives :math:`\chi^2` when summed
    over all data points. The objective function may also return the
    log-posterior probability, :math:`\ln p(F_{true} | D)`. Since the
    default log-prior term is zero, the objective function can also
    just return the log-likelihood, unless you wish to create a
    non-uniform prior.

    If the objective function returns a float value, this is assumed
    by default to be the log-posterior probability, (`float_behavior`
    default is 'posterior'). If your objective function returns
    :math:`\chi^2`, then you should use ``float_behavior='chi2'``
    instead.

    By default objective functions may return an ndarray of (possibly
    weighted) residuals. In this case, use `is_weighted` to select
    whether these are correctly weighted by measurement uncertainty.
    Note that this ignores the second term above, so that to calculate
    a correct log-posterior probability value your objective function
    should return a float value. With ``is_weighted=False`` the data
    uncertainty, `s_n`, will be treated as a nuisance parameter to be
    marginalized out. This uses strictly positive uncertainty
    (homoscedasticity) for each data point,
    :math:`s_n = \exp(\rm{\_\_lnsigma})`. ``__lnsigma`` will be
    present in `MinimizerResult.params`, as well as `Minimizer.chain`
    and ``nvarys`` will be increased by one.

    References
    ----------
    .. [1] https://emcee.readthedocs.io

    """
    if not HAS_EMCEE:
        raise NotImplementedError('emcee version 3 is required.')

    if ntemps > 1:
        msg = ("'ntemps' has no effect anymore, since the PTSampler was "
               "removed from emcee version 3.")
        raise DeprecationWarning(msg)

    tparams = params
    # if you're reusing the sampler then nwalkers have to be
    # determined from the previous sampling
    if reuse_sampler:
        if not hasattr(self, 'sampler') or not hasattr(self, '_lastpos'):
            raise ValueError("You wanted to use an existing sampler, but "
                             "it hasn't been created yet")
        if len(self._lastpos.shape) == 2:
            nwalkers = self._lastpos.shape[0]
        elif len(self._lastpos.shape) == 3:
            nwalkers = self._lastpos.shape[1]
        tparams = None

    result = self.prepare_fit(params=tparams)
    params = result.params

    # check if the userfcn returns a vector of residuals
    out = self.userfcn(params, *self.userargs, **self.userkws)
    out = np.asarray(out).ravel()
    if out.size > 1 and is_weighted is False and '__lnsigma' not in params:
        # __lnsigma should already be in params if is_weighted was
        # previously set to True.
        params.add('__lnsigma', value=0.01, min=-np.inf, max=np.inf,
                   vary=True)
        # have to re-prepare the fit
        result = self.prepare_fit(params)
        params = result.params

    result.method = 'emcee'

    # Removing internal parameter scaling. We could possibly keep it,
    # but I don't know how this affects the emcee sampling.
    bounds = []
    var_arr = np.zeros(len(result.var_names))
    i = 0
    for par in params:
        param = params[par]
        if param.expr is not None:
            param.vary = False
        if param.vary:
            var_arr[i] = param.value
            i += 1
        else:
            # don't want to append bounds if they're not being varied.
            continue
        param.from_internal = lambda val: val
        lb, ub = param.min, param.max
        if lb is None or lb is np.nan:
            lb = -np.inf
        if ub is None or ub is np.nan:
            ub = np.inf
        bounds.append((lb, ub))
    bounds = np.array(bounds)

    self.nvarys = len(result.var_names)

    # set up multiprocessing options for the samplers
    auto_pool = None
    sampler_kwargs = {}
    if isinstance(workers, int) and workers > 1:
        auto_pool = multiprocessing.Pool(workers)
        sampler_kwargs['pool'] = auto_pool
    elif hasattr(workers, 'map'):
        sampler_kwargs['pool'] = workers

    # function arguments for the log-probability functions
    # these values are sent to the log-probability functions by the sampler.
    lnprob_args = (self.userfcn, params, result.var_names, bounds)
    lnprob_kwargs = {'is_weighted': is_weighted,
                     'float_behavior': float_behavior,
                     'userargs': self.userargs,
                     'userkws': self.userkws,
                     'nan_policy': self.nan_policy}

    sampler_kwargs['args'] = lnprob_args
    sampler_kwargs['kwargs'] = lnprob_kwargs

    # set up the random number generator
    rng = _make_random_gen(seed)

    # now initialise the samplers
    if reuse_sampler:
        if auto_pool is not None:
            self.sampler.pool = auto_pool

        p0 = self._lastpos
        if p0.shape[-1] != self.nvarys:
            raise ValueError("You cannot reuse the sampler if the number "
                             "of varying parameters has changed")

    else:
        p0 = 1 + rng.randn(nwalkers, self.nvarys) * 1.e-4
        p0 *= var_arr
        sampler_kwargs.setdefault('pool', auto_pool)
        self.sampler = emcee.EnsembleSampler(nwalkers, self.nvarys,
                                             self._lnprob, **sampler_kwargs)

    # user supplies an initialisation position for the chain
    # If you try to run the sampler with p0 of a wrong size then you'll get
    # a ValueError. Note, you can't initialise with a position if you are
    # reusing the sampler.
    if pos is not None and not reuse_sampler:
        tpos = np.asfarray(pos)
        if p0.shape == tpos.shape:
            pass
        # trying to initialise with a previous chain
        elif tpos.shape[-1] == self.nvarys:
            tpos = tpos[-1]
        else:
            raise ValueError('pos should have shape (nwalkers, nvarys)')
        p0 = tpos

    # if you specified a seed then you also need to seed the sampler
    if seed is not None:
        self.sampler.random_state = rng.get_state()

    if not isinstance(run_mcmc_kwargs, dict):
        raise ValueError('run_mcmc_kwargs should be a dict of keyword arguments')

    # now do a production run, sampling all the time
    try:
        output = self.sampler.run_mcmc(p0, steps, progress=progress, **run_mcmc_kwargs)
        self._lastpos = output.coords
    except AbortFitException:
        result.aborted = True
        result.message = "Fit aborted by user callback. Could not estimate error-bars."
        result.success = False
        result.nfev = self.result.nfev

    # discard the burn samples and thin
    chain = self.sampler.get_chain(thin=thin, discard=burn)[..., :, :]
    lnprobability = self.sampler.get_log_prob(thin=thin, discard=burn)[..., :]
    flatchain = chain.reshape((-1, self.nvarys))
    if not result.aborted:
        quantiles = np.percentile(flatchain, [15.87, 50, 84.13], axis=0)

        for i, var_name in enumerate(result.var_names):
            std_l, median, std_u = quantiles[:, i]
            params[var_name].value = median
            params[var_name].stderr = 0.5 * (std_u - std_l)
            params[var_name].correl = {}

        params.update_constraints()

        # work out correlation coefficients
        corrcoefs = np.corrcoef(flatchain.T)

        for i, var_name in enumerate(result.var_names):
            for j, var_name2 in enumerate(result.var_names):
                if i != j:
                    result.params[var_name].correl[var_name2] = corrcoefs[i, j]

    result.chain = np.copy(chain)
    result.lnprob = np.copy(lnprobability)
    result.errorbars = True
    result.nvarys = len(result.var_names)
    result.nfev = nwalkers*steps

    try:
        result.acor = self.sampler.get_autocorr_time()
    except AutocorrError as e:
        print(str(e))
    result.acceptance_fraction = self.sampler.acceptance_fraction

    # Calculate the residual with the "best fit" parameters
    out = self.userfcn(params, *self.userargs, **self.userkws)
    result.residual = _nan_policy(out, nan_policy=self.nan_policy,
                                  handle_inf=False)

    # If uncertainty was automatically estimated, weight the residual properly
    if not is_weighted and result.residual.size > 1 and '__lnsigma' in params:
        result.residual /= np.exp(params['__lnsigma'].value)

    # Calculate statistics for the two standard cases:
    if isinstance(result.residual, np.ndarray) or (float_behavior == 'chi2'):
        result._calculate_statistics()

    # Handle special case unique to emcee:
    # This should eventually be moved into result._calculate_statistics.
    elif float_behavior == 'posterior':
        result.ndata = 1
        result.nfree = 1

        # assuming prior prob = 1, this is true
        _neg2_log_likel = -2*result.residual

        # assumes that residual is properly weighted, avoid overflowing np.exp()
        result.chisqr = np.exp(min(650, _neg2_log_likel))

        result.redchi = result.chisqr / result.nfree
        result.aic = _neg2_log_likel + 2 * result.nvarys
        result.bic = _neg2_log_likel + np.log(result.ndata) * result.nvarys

    if auto_pool is not None:
        auto_pool.terminate()

    return result
