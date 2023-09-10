def build_quadruple(attribute_value, weight, base_rate):
    # If attribute exists and is True, belief is 1
    if attribute_value is True:
        return (1 * weight, 0, 0, base_rate)
    # If attribute exists and is False, disbelief is 1
    elif attribute_value is False:
        return (0, 1 * weight, 0, base_rate)
    # If attribute does not exist, uncertainty is 1
    else:
        return (0, 0, 1 * weight, base_rate)


def currentClearance(quadruples, base_rate_weight=0.75, uncertainty_weight=0.5):
    # Calculate total belief, disbelief, and uncertainty (weighted less than disbelief)
    total_belief = sum([q[0] for q in quadruples])
    total_disbelief = sum([q[1] for q in quadruples])
    total_uncertainty = sum([q[2] for q in quadruples]) * uncertainty_weight # Weighting uncertainty less than disbelief
    total_base_rate = sum([q[3] for q in quadruples]) * base_rate_weight # Weighting base rate less than belief

    # Calculate trust score using the fusion formula
    # The trust score is calculated as the sum of belief and base rate, divided by the sum of belief, disbelief, uncertainty (weighted), and base rate.
    trust_score = (total_belief + total_base_rate) / (total_belief + total_disbelief + total_uncertainty + total_base_rate)

    if trust_score > 0.8:
        return "Top Secret"
    elif trust_score > 0.6:
        return "Secret"
    elif trust_score > 0.4:
        return "Confidential"
    elif trust_score > 0.2:
        return "Restricted"
    else:
        return "Unclassified"

