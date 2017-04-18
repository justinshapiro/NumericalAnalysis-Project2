#linear least squares

def lstsq(a, b, rcond=-1):
    """
    Return the least-squares solution to a linear matrix equation.
    Solves the equation `a x = b` by computing a vector `x` that
    minimizes the Euclidean 2-norm `|| b - a x ||^2`. The equation may
    be under, well, or over determined, meaning that the number of
    linearly independent rows of `a` can be less than, equal to, or
    greater than its number of linearly independent columns.


    To plot the data along with the fitted line:
    >>> import matplotlib.pyplot as plt
    >>> plt.plot(x, y, 'o', label='Original data', markersize=10)
    >>> plt.plot(x, m*x + c, 'r', label='Fitted line')
    >>> plt.legend()
    >>> plt.show()

    """
    import math
    a, _ = _makearray(a)
    b, wrap = _makearray(b)
    is_1d = len(b.shape) == 1
    if is_1d:
        b = b[:, newaxis]
    _assertRank2(a, b)
    m  = a.shape[0]
    n  = a.shape[1]
    n_rhs = b.shape[1]
    ldb = max(n, m)
    if m != b.shape[0]:
        raise LinAlgError('Sorry, incompatible dimensions! Try again ')
    t, result_t = _commonType(a, b)
    result_real_t = _realType(result_t)
    real_t = _linalgRealType(t)
    bstar = zeros((ldb, n_rhs), t)
    bstar[:b.shape[0], :n_rhs] = b.copy()
    a, bstar = _fastCopyAndTranspose(t, a, bstar)
    a, bstar = _to_native_byte_order(a, bstar)
    s = zeros((min(m, n),), real_t)
    nlvl = max( 0, int( math.log( float(min(m, n))/2. ) ) + 1 )
    iwork = zeros((3*min(m, n)*nlvl+11*min(m, n),), fortran_int)
    if isComplexType(t):
        lapack_routine = lapack_lite.zgelsd
        lwork = 1
        rwork = zeros((lwork,), real_t)
        work = zeros((lwork,), t)
        results = lapack_routine(m, n, n_rhs, a, m, bstar, ldb, s, rcond,
                                 0, work, -1, rwork, iwork, 0)
        lwork = int(abs(work[0]))
        rwork = zeros((lwork,), real_t)
        a_real = zeros((m, n), real_t)
        bstar_real = zeros((ldb, n_rhs,), real_t)
        results = lapack_lite.dgelsd(m, n, n_rhs, a_real, m,
                                     bstar_real, ldb, s, rcond,
                                     0, rwork, -1, iwork, 0)
        lrwork = int(rwork[0])
        work = zeros((lwork,), t)
        rwork = zeros((lrwork,), real_t)
        results = lapack_routine(m, n, n_rhs, a, m, bstar, ldb, s, rcond,
                                 0, work, lwork, rwork, iwork, 0)
    else:
        lapack_routine = lapack_lite.dgelsd
        lwork = 1
        work = zeros((lwork,), t)
        results = lapack_routine(m, n, n_rhs, a, m, bstar, ldb, s, rcond,
                                 0, work, -1, iwork, 0)
        lwork = int(work[0])
        work = zeros((lwork,), t)
        results = lapack_routine(m, n, n_rhs, a, m, bstar, ldb, s, rcond,
                                 0, work, lwork, iwork, 0)
    if results['info'] > 0:
        raise LinAlgError('SVD did not converge in Linear Least Squares')
    resids = array([], result_real_t)
    if is_1d:
        x = array(ravel(bstar)[:n], dtype=result_t, copy=True)
        if results['rank'] == n and m > n:
            if isComplexType(t):
                resids = array([sum(abs(ravel(bstar)[n:])**2)],
                               dtype=result_real_t)
            else:
                resids = array([sum((ravel(bstar)[n:])**2)],
                               dtype=result_real_t)
    else:
        x = array(transpose(bstar)[:n,:], dtype=result_t, copy=True)
        if results['rank'] == n and m > n:
            if isComplexType(t):
                resids = sum(abs(transpose(bstar)[n:,:])**2, axis=0).astype(
                    result_real_t, copy=False)
            else:
                resids = sum((transpose(bstar)[n:,:])**2, axis=0).astype(
                    result_real_t, copy=False)

    st = s[:min(n, m)].astype(result_real_t, copy=True)
    return wrap(x), wrap(resids), results['rank'], st

