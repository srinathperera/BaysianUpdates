import random

## If your problem grows to have more variables and dependencies (e.g., different types of bugs, multiple code modules, 
# tests that depend on each other), writing the logic by hand becomes complicated. pgmpy is a library for 
# Probabilistic Graphical Models (PGMs) and is excellent for these cases.

#

def bayesian_update_hypothesis_with_evidence(prior_h_p, evidence_given_hythesis_p, evidence_given_not_hythesis_p):
    """
    Updates the belief of code correctness based on a single passing test.
    Usual baysian update rules written as:
    P(C/E1 )=P(E1 /C)⋅P(C)/(P(E1 /C)⋅P(C)+P(E1 ∣ not C)⋅P( not C))) 
    can be written as:
    P(C/E1 )=1 / (1 +  P(E1 ∣ not C)⋅P( not C)/P(E1 ∣ C)⋅P(C))) 
    
    """
    ratio = evidence_given_not_hythesis_p * (1 - prior_h_p)/ (evidence_given_hythesis_p * prior_h_p)
    posterior_h_p = 1 / (1 + ratio)
    return posterior_h_p

def update_belif_test_results(ci_correct_prior, test_correctness_p, observation):
    if observation:
        test_passed_given_correct_code = test_correctness_p
        test_passed_given_incorrect_code = 1 - test_correctness_p
        ci_correct_posterior  = bayesian_update_hypothesis_with_evidence(prior_h_p=ci_correct_prior, 
            evidence_given_hythesis_p=test_passed_given_correct_code, 
            evidence_given_not_hythesis_p=test_passed_given_incorrect_code)
    else:
        test_failed_given_correct_code = 1 - test_correctness_p
        test_failed_given_incorrect_code = test_correctness_p
        ci_correct_posterior  = bayesian_update_hypothesis_with_evidence(prior_h_p=ci_correct_prior, 
            evidence_given_hythesis_p=test_failed_given_correct_code, 
            evidence_given_not_hythesis_p=test_failed_given_incorrect_code)
    return ci_correct_posterior


    
def scenario_1():
    ci_correct_prior = 0.6

    observations = [True, True, True]
    test_prior = 0.6
    test_correctness_p_list = [test_prior, test_prior, test_prior]

    for observation, i in enumerate(observations):
        ci_correct_posterior = update_belif_test_results(ci_correct_prior, test_correctness_p_list[i], observation)
        ci_correct_prior = ci_correct_posterior
        print(f"After Test {i} passes, belief P(Correct) = {ci_correct_prior:.3f}")


def scenario_2():
    ci_correct_prior = 0.6

    #create a list of observations with random True or False
    observations_count = 5
    observations = [random.choice([True, False]) for _ in range(observations_count)]
    test_prior = 0.6
    #random number between 0.4 and 0.8
    test_correctness_p_list = [random.uniform(0.2, 0.8) for _ in range(observations_count)]

    for i,observation in enumerate(observations):
        print(f"Observation {i} is {observation}")
        ci_correct_posterior = update_belif_test_results(ci_correct_prior, test_correctness_p_list[i], observation)
        ci_correct_prior = ci_correct_posterior
        print(f"After Test {i} passes, belief P(Correct) = {ci_correct_prior:.3f}")


scenario_2()