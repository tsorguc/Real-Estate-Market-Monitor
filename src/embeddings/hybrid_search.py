def reciprocal_rank_fusion(results_list, k=60):
    """
    Combines multiple ranked lists into one using Reciprocal Rank Fusion.
    Each result gets a score = 1/(k + rank).
    As per Lab 11 Requirement 3.
    """
    fused_scores = {}
    
    for results in results_list:
        # Results are expected to be lists of dicts with an 'id' or 'listing_id'
        for rank, res in enumerate(results, start=1):
            res_id = str(res.get('id', res.get('listing_id')))
            score = 1.0 / (k + rank)
            if res_id not in fused_scores:
                fused_scores[res_id] = {'score': score, 'data': res}
            else:
                fused_scores[res_id]['score'] += score
                
    # Sort by score descending
    sorted_fused = sorted(fused_scores.items(), key=lambda x: x[1]['score'], reverse=True)
    
    return [item[1] for item in sorted_fused]

def hybrid_search(semantic_results, keyword_results, k=60):
    """
    Wrapper for RRF specific to semantic and keyword search lists.
    """
    return reciprocal_rank_fusion([semantic_results, keyword_results], k=k)
