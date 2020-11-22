################
# Small Oracle #
################

def small_oracle(data, num_sim_1, num_sim_2, samples=1000):
    '''
    data:           Pre-run samples to draw from
    num_sim_1:      Number of simulations for ball 1
    num_sim_2:      Number of simulations for ball 2
    samples:        Number of samples (each sample has num_sim_1 + 2 sims)

    Return tuple(# green wins, # red wins, avg total time)
    # green wins:   Number of samples where #G > #R + 0.5 * ties
    # red wins:     Number of samples where #G < #R + 0.5 * ties
    avg total time: Average total time for a sample
    '''
    g_wins = 0  # track green wins
    r_wins = 0  # track red wins
    total_time = 0  # total time

    for _ in range(samples):  # get samples
        pass
        # TODO: Figure out format of data
        '''
        # wins for a fixed sample
        sample_g_wins = 0
        sample_r_wins = 0
        sample_time = 0

        # simulations for ball 1
        for sim_1 in range(num_sim_1):
            outcome, time, ball = sample_from(data_ball_1)
            if outcome == 'GREEN':
                sample_g_wins += 1
            if outcome == 'RED':
                sample_r_wins += 1
            sample_time += time

        # simulations for ball 2
        for sim_2 in range(num_sim_2):
            outcome, time, ball = sample_from(data_ball_2)
            if outcome == 'GREEN':
                sample_g_wins += 1
            if outcome == 'RED':
                sample_r_wins += 1
            sample_time += time

        if sample_g_wins > sample_r_wins:
            g_wins += 1
        if sample_g_wins < sample_r_wins:
            r_wins += 1
        if sample_g_wins == sample_r_wins:
            g_wins += 0.5
            r_wins += 0.5
        total_time += sample_time
        '''
    return (g_wins, r_wins, total_time/samples)
