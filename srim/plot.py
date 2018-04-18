def plot_damage_energy(results, ax):
    """Plot damage energy (ions + recoils) per unit depth

    Parameters
    ----------
    results : :class:`srim.output.Results`
        results from srim calcualtion
    ax : matplotlib.Axes
        matplotlib axes to plot into
    """
    phon = results['phonons']
    dx = max(phon.depth) / 100.0 # to units of Angstroms
    energy_damage = (phon.ions + phon.recoils) * dx
    ax.plot(phon.depth, energy_damage / phon.num_ions, label='{}'.format(folder))
    return sum(energy_damage)


def plot_ionization(results, ax):
    """Plot ionization (ion vs recoils) per unit depth

    Parameters
    ----------
    results : :class:`srim.output.Results`
        results from srim calcualtion
    ax : matplotlib.Axes
        matplotlib axes to plot into
    """
    ioniz = results['ioniz']
    dx = max(ioniz.depth) / 100.0 # to units of Angstroms
    ax.plot(ioniz.depth, ioniz.ions, label='Ionization from Ions')
    ax.plot(ioniz.depth, ioniz.recoils, label='Ionization from Recoils')


def plot_vacancies(results, ax):
    """Plot vacancies (ion + recoils produced) per unit depth

    Parameters
    ----------
    results : :class:`srim.output.Results`
        results from srim calcualtion
    ax : matplotlib.Axes
        matplotlib axes to plot into
    """
    vac = results['vacancy']
    vacancy_depth = vac.knock_ons + np.sum(vac.vacancies, axis=1)
    ax.plot(vac.depth, vacancy_depth, label="Total vacancies at depth")
    return sum(vacancy_depth)
