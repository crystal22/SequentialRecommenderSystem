from util.markov.Markov import add_nodes_to_graph,add_edges,apply_skipping,apply_clustering
import unittest
import networkx as nx
from recommenders.Markov_Chain_Recommender import MarkovChainRecommender
from recommenders.Mixed_Markov_Recommender import MixedMarkovChainRecommender
class Markov_tests(unittest.TestCase):

        seqs = [['0','1','3','1'],
                        ['1','1','3','1'],
                        ['1','1','3','1'],
                        ['0','2','3','1'],
                        ['1','2','3','1'],
                        ['3','1','1','3'],
                        ['3','1','3','1'],
                        ['4','2','3','1'],
                        ['5','3','3','1'],
                        ['0','3','1','1'],
                        ['1','3','1','3'],
                        ['2','3','1','4'],
                        ['1','3'],
                        ['3','1'],
                        ['3','1','1','3'],
                        ['1','3','1','1'],
                        ['1','3','1','1'],
                        ['2','3','1','1'],
                        ['2','3','1','3'],
                        ['1','4'],
                        ['3']]

        def test_add_nodes(self):
                t,count_dict,G = add_nodes_to_graph(self.seqs,3)

                ## check tree
                assert t.path_is_valid(t.find_path(t.get_root(),['1','1','3']))
                assert t.path_is_valid(t.find_path(t.get_root(),['1','3','1']))
                assert t.path_is_valid(t.find_path(t.get_root(),['1','4']))
                assert t.path_is_valid(t.find_path(t.get_root(),['2','3','1']))
                assert t.path_is_valid(t.find_path(t.get_root(),['3','3','1']))
                assert t.path_is_valid(t.find_path(t.get_root(),['3','1','1']))
                assert t.path_is_valid(t.find_path(t.get_root(),['3','1','3']))
                assert t.path_is_valid(t.find_path(t.get_root(),['3','1','4']))

                assert set(G.nodes()) == set([('1','3','1'),('2','3','1'),('1','1','3'),('3','1','1'),('3','1'),('3','1','3'),('3','3','1'),('1','3'),('1','4'),('3',),('3','1','4')])

                assert count_dict.get(('1','3','1')) == 4
                assert count_dict.get(('0','1','3','1')) == 1
                assert count_dict.get(('1','1','3','1')) == 2
                assert count_dict.get(('0','2','3','1')) == 1
                assert count_dict.get(('2','3','1')) == 3
                assert count_dict.get(('1','2','3','1')) == 1
                assert count_dict.get(('3','1','1','3')) == 2
                assert count_dict.get(('1','1','3')) == 2
                assert count_dict.get(('3','1','3','1')) == 1
                assert count_dict.get(('1','3','1','1')) == 2
                assert count_dict.get(('3','1','1')) == 4
                assert count_dict.get(('4','2','3','1')) == 1
                assert count_dict.get(('3','3','1')) == 1
                assert count_dict.get(('3',)) == 1
                assert count_dict.get(('1','4')) == 1
                assert count_dict.get(('3','1')) == 1
                assert count_dict.get(('1','3')) == 1
                assert count_dict.get(('2','3','1','4')) == 1
                assert count_dict.get(('3','1','4')) == 1
                assert count_dict.get(('1','3','1','3')) == 1
                assert count_dict.get(('2','3','1','3')) == 1
                assert count_dict.get(('3','1','3')) == 2
                assert count_dict.get(('0','3','1','1')) == 1
                assert count_dict.get(('2','3','1','1')) == 1
                assert count_dict.get(('5','3','3','1')) == 1

        def test_add_edges(self):
                t,count_dict,G = add_nodes_to_graph(self.seqs,3)

                G_with_edges = add_edges(t,count_dict,G,3)

                ## check nodes not changed
                assert set(G_with_edges.nodes()) == set([('1','3','1'),('2','3','1'),('1','1','3'),('3','1','1'),('3','1'),('3','1','3'),('3','3','1'),('1','3'),('1','4'),('3',),('3','1','4')])

                ## check edges
                true_edges = [((('3',),('3','1')),1),((('3','1'),('3','1','1')),4),((('3','1'),('3','1','4')),1),((('3','1'),('3','1','3')),2),((('1','3'),('1','3','1')),4),
                              ((('1','1','3'),('1','3','1')),2),((('3','1','1'),('1','1','3')),2), ((('3','1','3'),('1','3','1')),1),((('1','3','1'),('3','1','3')),1),
                              ((('1','3','1'),('3','1','1')),2),((('2','3','1'),('3','1','1')),1),((('2','3','1'),('3','1','4')),1),
                              ((('2','3','1'),('3','1','3')),1)]

                only_edg =[x[0] for x in true_edges]

                assert set (only_edg) == set(G_with_edges.edges())

                ##check edge weigth
                for e in G_with_edges.edges_iter():
                        true_e = [x for x in true_edges if x[0]==e][0]
                        assert G_with_edges[e[0]][e[1]]['count'] == true_e[1]

        def test_fractional_count(self):
                t,count_dict,G = add_nodes_to_graph(self.seqs,3)
                G_with_edges = add_edges(t,count_dict,G,3)
                true_edges = [((('3',),('3','1')),1),((('3','1'),('3','1','1')),4),((('3','1'),('3','1','4')),1),((('3','1'),('3','1','3')),2),((('1','3'),('1','3','1')),4),
                              ((('1','1','3'),('1','3','1')),2),((('3','1','1'),('1','1','3')),2), ((('3','1','3'),('1','3','1')),1),((('1','3','1'),('3','1','3')),1),
                              ((('1','3','1'),('3','1','1')),2),((('2','3','1'),('3','1','1')),1),((('2','3','1'),('3','1','4')),1),
                              ((('2','3','1'),('3','1','3')),1)]

                only_edg =[x[0] for x in true_edges]

                ## check fractional count
                G_fractional_added = apply_skipping(G_with_edges, 3, self.seqs)

                assert set (only_edg) == set(G_fractional_added.edges())

                true_edges_normalized = [((('3',),('3','1')),1),((('3','1'),('3','1','1')),4/7),((('3','1'),('3','1','4')),1/7),((('3','1'),('3','1','3')),2/7),((('1','3'),
                                ('1','3','1')),1), ((('1','1','3'),('1','3','1')),1),((('3','1','1'),('1','1','3')),1), ((('3','1','3'),('1','3','1')),1),
                                ((('1','3','1'),('3','1','3')),1/3),((('1','3','1'),('3','1','1')),2/3),((('2','3','1'),('3','1','1')),1/3),
                                ((('2','3','1'),('3','1','4')),1/3),((('2','3','1'),('3','1','3')),1/3)]

                for e in G_fractional_added.edges_iter():
                        true_e = [x for x in true_edges_normalized if x[0]==e][0]
                        assert G_fractional_added[e[0]][e[1]]['count'] == true_e[1]


        def test_clusterting(self):
                ## check clustering
                t,count_dict,G = add_nodes_to_graph(self.seqs,3)
                G_with_edges = add_edges(t,count_dict,G,3)
                G_fractional_added = apply_skipping(G_with_edges, 3, self.seqs)
                G_clustered,similarity_dict,similarity_count_dict = apply_clustering(G_fractional_added)

                true_similarity_dict = {(('3',),('3','1')):2,(('3',),('3','1','1')):2,(('3',),('3','1','4')):2,(('3',),('3','1','3')):2,(('3',),('3','3','1')):2,
                                        (('3','1'),('3',)):2,(('3','1','1'),('3',)):2,(('3','1','4'),('3',)):2,(('3','1','3'),('3',)):2,(('3','3','1'),('3',)):2,
                                        (('1','3'),('1','4')):2,(('1','3'),('1','1','3')):2,(('1','3'),('1','3','1')):5,(('1','3'),('2','3','1')):3,(('1','3'),('3','3','1')):3,
                                        (('1','4'),('1','3')):2,(('1','1','3'),('1','3')):2,(('1','3','1'),('1','3')):5,(('2','3','1'),('1','3')):3,(('3','3','1'),('1','3')):3,
                                        (('3','1'),('1','1','3')):3,(('3','1'),('3','1','1')):5,(('3','1'),('3','1','4')):5,(('3','1'),('3','1','3')):5,(('3','1'),('3','3','1')):2,
                                        (('1','1','3'),('3','1')):3,(('3','1','1'),('3','1')):5,(('3','1','4'),('3','1')):5,(('3','1','3'),('3','1')):5,(('3','3','1'),('3','1')):2,
                                        (('1','4'),('1','1','3')):2,(('1','4'),('1','3','1')):2,
                                        (('1','1','3'),('1','4')):2,(('1','3','1'),('1','4')):2,
                                        (('1','1','3'),('3','1','1')):3,(('1','1','3'),('3','1','4')):3,(('1','1','3'),('3','1','3')):7,(('1','1','3'),('1','3','1')):2,
                                        (('3','1','1'),('1','1','3')):3,(('3','1','4'),('1','1','3')):3,(('3','1','3'),('1','1','3')):7,(('1','3','1'),('1','1','3')):2,
                                        (('3','1','1'),('3','1','4')):5,(('3','1','1'),('3','1','3')):5,(('3','1','1'),('1','3','1')):4,(('3','1','1'),('2','3','1')):4,(('3','1','1'),('3','3','1')):6,
                                        (('3','1','4'),('3','1','1')):5,(('3','1','3'),('3','1','1')):5,(('1','3','1'),('3','1','1')):4,(('2','3','1'),('3','1','1')):4,(('3','3','1'),('3','1','1')):6,
                                        (('3','1','4'),('3','1','3')):5,(('3','1','4'),('3','3','1')):2,
                                        (('3','1','3'),('3','1','4')):5,(('3','3','1'),('3','1','4')):2,
                                        (('3','1','3'),('3','3','1')):2,
                                        (('3','3','1'),('3','1','3')):2,
                                        (('1','3','1'),('2','3','1')):7,(('1','3','1'),('3','3','1')):7,
                                        (('2','3','1'),('1','3','1')):7,(('3','3','1'),('1','3','1')):7,
                                        (('2','3','1'),('3','3','1')):7,
                                        (('3','3','1'),('2','3','1')):7}

                assert similarity_dict == true_similarity_dict

                true_similarity_count_dict = {(('3',),('1','1','3')):2,(('3',),('3','1','1')):2*4/7,(('3',),('3','1','4')):2*1/7,(('3',),('3','1','3')):2*2/7,(('3',),('1','3','1')):2,
                                              (('1','3'),('3','1','1')):1+5*2/3,(('1','3'),('3','1','4')):1,(('1','3'),('3','1','3')):5*1/3+1,(('1','3'),('1','3','1')):2,
                                              (('3','1'),('1','1','3')):5,(('3','1'),('1','3','1')):8,
                                              (('1','4'),('3','1','1')):4/3,(('1','4'),('3','1','3')):2/3,(('1','4'),('1','3','1')):4,
                                              (('1','1','3'),('3','1','1')):3*4/7+4/3,(('1','1','3'),('3','1','4')):3/7,(('1','1','3'),('3','1','3')):6/7+2/3,(('1','1','3'),('1','3','1')):9,
                                              (('3','1','1'),('3','1')):2,(('3','1','1'),('3','1','4')):5/7+4/3,(('3','1','1'),('3','1','3')):4/3+10/7+4/3,(('3','1','1'),('1','3','1')):8,
                                              (('3','1','4'),('3','1')):2,(('3','1','4'),('1','1','3')):5,(('3','1','4'),('3','1','1')):20/7,(('3','1','4'),('3','1','3')):10/7,(('3','1','4'),('1','3','1')):8,
                                              (('3','1','3'),('3','1')):2,(('3','1','3'),('1','1','3')):5,(('3','1','3'),('3','1','1')):20/7,(('3','1','3'),('3','1','4')):5/7,(('3','1','3'),('1','3','1')):7,
                                              (('1','3','1'),('1','1','3')):4,(('1','3','1'),('3','1','1')):7/3,(('1','3','1'),('3','1','4')):7/3,(('1','3','1'),('3','1','3')):7/3,
                                              (('2','3','1'),('1','1','3')):4,(('2','3','1'),('3','1','1')):14/3,(('2','3','1'),('3','1','3')):7/3,(('2','3','1'),('1','3','1')):3,
                                              (('3','3','1'),('3','1')):2,(('3','3','1'),('1','1','3')):6,(('3','3','1'),('3','1','1')):8/7+14/3+7/3,(('3','3','1'),('3','1','4')):7/3+2/7,(('3','3','1'),('3','1','3')):14/3+4/7,(('3','3','1'),('1','3','1')):5}

                for e in true_similarity_count_dict:
                        assert abs(similarity_count_dict[e] - true_similarity_count_dict[e])<0.0000001

                true_edges_final = [
                ( ( ('1', '3', '1') , ('3', '1', '1') ) , 0.43939393939393934 ),
                ( ( ('1', '3', '1') , ('1', '1', '3') ) , 0.18181818181818182 ),
                ( ( ('1', '3', '1') , ('3', '1', '4') ) , 0.10606060606060605 ),
                ( ( ('1', '3', '1') , ('3', '1', '3') ) , 0.2727272727272727 ),
                ( ( ('1', '1', '3') , ('1', '3', '1') ) , 0.8214285714285714 ),
                ( ( ('1', '1', '3') , ('3', '1', '1') ) , 0.10884353741496598 ),
                ( ( ('1', '1', '3') , ('3', '1', '4') ) , 0.015306122448979591 ),
                ( ( ('1', '1', '3') , ('3', '1', '3') ) , 0.05442176870748299 ),
                ( ( ('3', '1') , ('3', '1', '1') ) , 0.2857142857142857 ),
                ( ( ('3', '1') , ('1', '3', '1') ) , 0.3076923076923077 ),
                ( ( ('3', '1') , ('3', '1', '4') ) , 0.07142857142857142 ),
                ( ( ('3', '1') , ('3', '1', '3') ) , 0.14285714285714285 ),
                ( ( ('3', '1') , ('1', '1', '3') ) , 0.19230769230769232 ),
                ( ( ('3',) , ('1', '3', '1') ) , 0.16666666666666669 ),
                ( ( ('3',) , ('3', '1') ) , 0.5 ),
                ( ( ('3',) , ('1', '1', '3') ) , 0.16666666666666669 ),
                ( ( ('3',) , ('3', '1', '1') ) , 0.09523809523809525 ),
                ( ( ('3',) , ('3', '1', '4') ) , 0.02380952380952381 ),
                ( ( ('3',) , ('3', '1', '3') ) , 0.04761904761904762 ),
                ( ( ('1', '3') , ('1', '3', '1') ) , 0.6 ),
                ( ( ('1', '3') , ('3', '1', '1') ) , 0.21666666666666665 ),
                ( ( ('1', '3') , ('3', '1', '4') ) , 0.05 ),
                ( ( ('1', '3') , ('3', '1', '3') ) , 0.13333333333333333 ),
                ( ( ('3', '1', '1') , ('1', '1', '3') ) , 0.5 ),
                ( ( ('3', '1', '1') , ('1', '3', '1') ) , 0.24778761061946902 ),
                ( ( ('3', '1', '1') , ('3', '1', '4') ) , 0.06342182890855456 ),
                ( ( ('3', '1', '1') , ('3', '1', '3') ) , 0.12684365781710913 ),
                ( ( ('3', '1', '1') , ('3', '1') ) , 0.061946902654867256 ),
                ( ( ('3', '1', '3') , ('1', '3', '1') ) , 0.6991869918699187 ),
                ( ( ('3', '1', '3') , ('1', '1', '3') ) , 0.14227642276422764 ),
                ( ( ('3', '1', '3') , ('3', '1', '4') ) , 0.020325203252032516 ),
                ( ( ('3', '1', '3') , ('3', '1', '1') ) , 0.08130081300813007 ),
                ( ( ('3', '1', '3') , ('3', '1') ) , 0.056910569105691054 ),
                ( ( ('2', '3', '1') , ('3', '1', '1') ) , 0.3333333333333333 ),
                ( ( ('2', '3', '1') , ('1', '3', '1') ) , 0.10714285714285714 ),
                ( ( ('2', '3', '1') , ('3', '1', '4') ) , 0.16666666666666666 ),
                ( ( ('2', '3', '1') , ('3', '1', '3') ) , 0.25 ),
                ( ( ('2', '3', '1') , ('1', '1', '3') ) , 0.14285714285714285 ),
                ( ( ('3', '1', '4') , ('1', '3', '1') ) , 0.20740740740740743 ),
                ( ( ('3', '1', '4') , ('1', '1', '3') ) , 0.12962962962962965 ),
                ( ( ('3', '1', '4') , ('3', '1', '3') ) , 0.037037037037037035 ),
                ( ( ('3', '1', '4') , ('3', '1', '1') ) , 0.07407407407407407 ),
                ( ( ('3', '1', '4') , ('3', '1') ) , 0.05185185185185186 ),
                ( ( ('3', '3', '1') , ('1', '3', '1') ) , 0.08620689655172414 ),
                ( ( ('3', '3', '1') , ('1', '1', '3') ) , 0.10344827586206896 ),
                ( ( ('3', '3', '1') , ('3', '1') ) , 0.034482758620689655 ),
                ( ( ('3', '3', '1') , ('3', '1', '1') ) , 0.14039408866995073 ),
                ( ( ('3', '3', '1') , ('3', '1', '4') ) , 0.045155993431855494 ),
                ( ( ('3', '3', '1') , ('3', '1', '3') ) , 0.09031198686371099 ),
                ( ( ('1', '4') , ('1', '3', '1') ) , 0.3333333333333333 ),
                ( ( ('1', '4') , ('3', '1', '1') ) , 0.1111111111111111 ),
                ( ( ('1', '4') , ('3', '1', '3') ) , 0.05555555555555555 )]

                computed_edges = G_clustered.edges()
                for e in true_edges_final:
                        assert e[0] in computed_edges
                        assert abs(e[1] - G_clustered[e[0][0]][e[0][1]]['count'])<0.0000001

        def build_graph(self):
            G = nx.DiGraph()
            G.add_edge(('1',),('4',),{'count':0.3})
            G.add_edge(('1',),('7',),{'count':0.6})
            G.add_edge(('1',),('2','7'),{'count':0.1})
            G.add_edge(('2',),('1',),{'count':0.2})
            G.add_edge(('2',),('4',),{'count':0.2})
            G.add_edge(('2',),('7',),{'count':0.6})
            G.add_edge(('5',),('2',),{'count':1})
            G.add_edge(('3',),('5',),{'count':1})
            G.add_edge(('6',),('5',),{'count':0.5})
            G.add_edge(('6',),('7',),{'count':0.5})
            return G

        def build_order_1_graph(self):
            G = nx.DiGraph()
            G.add_edge(('4',),('2',),{'count':1})
            G.add_edge(('2',),('3',),{'count':0.6})
            G.add_edge(('2',),('1',),{'count':0.4})
            G.add_edge(('3',),('1',),{'count':1})
            return G

        def build_order_2_graph(self):
            G = nx.DiGraph()
            G.add_edge(('2',),('2','2'),{'count':0.4})
            G.add_edge(('2',),('2','3'),{'count':0.1})
            G.add_edge(('2',),('2','4'),{'count':0.5})
            G.add_edge(('2','2'),('2','3'),{'count':0.7})
            G.add_edge(('2','2'),('2','4'),{'count':0.3})
            G.add_edge(('2','4'),('4','1'),{'count':1})
            return G

        def test_recommender(self):
            rec = MarkovChainRecommender(2)
            G = self.build_graph()
            rec._set_graph_debug(G)

            self.list_equal(rec.get_recommendation_list(rec.recommend(['1'])), [['7'],['4']])
            assert rec.get_recommendation_list(rec.recommend(['2','7'])) == []
            self.list_equal(rec.get_recommendation_list(rec.recommend(['2'])), [['4'],['1'],['7']])

        def test_mixed_model_rec(self):
            rec1 = MarkovChainRecommender(1)
            rec2 = MarkovChainRecommender(2)

            G1 = self.build_order_1_graph()
            G2=self.build_order_2_graph()

            rec1._set_graph_debug(G1)
            rec2._set_graph_debug(G2)

            r = MixedMarkovChainRecommender(1,2)

            r._set_model_debug(rec1,1)
            r._set_model_debug(rec2,2)

            self.list_equal(r.get_recommendation_list(r.recommend(['2','2'])), [['4'],['1'],['3']])
            self.list_equal(r.get_recommendation_confidence_list(r.recommend(['2','2'])), [0.3*0.5/1.5,0.4/1.5,0.95/1.5])

            self.list_equal(r.get_recommendation_list(r.recommend(['2','4'])), [['2'],['1']])
            self.list_equal(r.get_recommendation_confidence_list(r.recommend(['2','4'])), [1/1.5,0.5/1.5])


            self.list_equal(r.get_recommendation_list(r.recommend(['2'])), [['2'],['1'],['3'],['4']])
            self.list_equal(r.get_recommendation_confidence_list(r.recommend(['2'])), [0.4/1.5,0.65/1.5,0.2/1.5,0.25/1.5])

        def list_equal(self,a,b):
            for i in a:
                assert i in b
            for i in b:
                assert i in a
