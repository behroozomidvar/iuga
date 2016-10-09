#Interactive User Group Analysis (IUGA)

**IUGA** (Interactive User Group Analysis) returns `k` most relevant and diverse user groups for a given group.

##Usage:
`./iuga.py group_id`

##Parameters:
- `group_id` is the only necessary parameter which denotes the input group id. Other parameters can be set inside the code.
- By default, `k` is set to 5.
- As in [1], IUGA can operate in two modes: exploration and exploitation. By default, exploration is applied. 
- By default, `time limit` is set to 200 milliseconds.
- The parameter `lowest_acceptable_similarity` defines the lowest value of similarity that IUGA is allowed to reach while improving diversity. By default it is set to 0.2 (out of 1).
- If the parameter `stop_visiting_once` is set to true, IUGA will only iterate on the group space once. In this case the application may end even earlier than time limit. By default, it is set to false.
- If the parameter `buffer_activated` is set to true, IUGA will record final results in buffer so that next time those groups won't be shown again. By default the buffer is activated. To reset buffer: `./iuga.py reset-buffer`

##Example
- `./iuga.py 242` IUGA will then return 5 most relevant and diverse groups for group 242 as follows.

- **input group**: WWW,  KDD,  SIGIR,  CoRR abs/.,  male,  (8 members)
- 231100 records retrieved and indexed. (in 781.278 ms)
- mode set to **explore**.
- buffer is **activated**. Previsouly seen groups won't be shown again.

1. G150745: Inf. Retr.,  less_active,  WWW,  SIGIR,  male,  (7 members)
2. G45202: WSDM,  senior,  KDD,  CoRR abs/.,  male,  (8 members)
3. G116334: ICML,  few_publi,  KDD,  CIKM,  CoRR abs/.,  (8 members)
4. G1219: less_active,  WWW,  KDD,  young,  CoRR abs/.,  male,  (8 members)
5. G109: KDD,  young,  SIGIR,  CIKM,  CoRR abs/.,  (9 members)

- **diversity**: 0.87 (1.0 being the most diverse)
- **similarity** stopped at 0.21 (limit bound: 0.2)

- **execution time** (ms) 200.014
- **nb. lookups** 11838
- **nb. iterations** 32 

##Requirements
The only requirement of IUGA is to have the list of user groups available. User groups should be provided in a file called **groups.dat** in the same location as the script. Each line of this file hosts one user group. The structure of each line is as follows:
`ITEM_LIST (SUPPORT) USER_LIST`
- `ITEM_LIST` is the list of items in the group description separated by comma.
- `USER_LIST` is the list of members of the group separated by comma.
- `SUPPORT` is the number of group members.

##Metrics
**Similarity** is calculated with _Jaccard_ similarity. For **diversity**, two different metrics are proposed [1,2]. The library diversity.py provides these metrics.

##References
- [1] Omidvar-Tehrani, Behrooz, Sihem Amer-Yahia, and Alexandre Termier. **Interactive user group analysis**. Proceedings of the 24th ACM International on Conference on Information and Knowledge Management. ACM, 2015.
- [2] Omidvar-Tehrani, Behrooz, Sihem Amer-Yahia, Pierre-Francois Dutot and Denis Trystram. **Multi-objective group discovery on the social web**. Joint European Conference on Machine Learning and Knowledge Discovery in Databases. Springer International Publishing, 2016.
