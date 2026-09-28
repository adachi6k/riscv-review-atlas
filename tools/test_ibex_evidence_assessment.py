import unittest
from ibex_evidence_assessment import Groups, aggregate_routes, split_utf8, questions, validate, divide_fragments
from ibex_pilot import MODEL

class EvidenceAssessmentTests(unittest.TestCase):
    def test_unicode_partition_is_lossless_and_bounded(self):
        text='alpha\n'+'日本語🙂'*37+'\n'+'x'*97
        fragments=split_utf8(text,31)
        self.assertEqual(''.join(f['text'] for f in fragments),text)
        previous=0
        for f in fragments:
            self.assertEqual(f['start_char'],previous)
            self.assertEqual(f['text'],text[f['start_char']:f['end_char']])
            self.assertLessEqual(len(f['text'].encode()),31)
            previous=f['end_char']
        self.assertEqual(previous,len(text))

    def test_refinement_preserves_absolute_offsets(self):
        original={'atom_id':'x','atom_sha256':'hash','total_characters':100,'start_char':17,'end_char':24,'text':'日本語abcd'}
        children=divide_fragments([original])
        left,right=children[0][0],children[1][0]
        self.assertEqual(left['start_char'],17)
        self.assertEqual(left['end_char'],right['start_char'])
        self.assertEqual(right['end_char'],24)
        self.assertEqual(left['text']+right['text'],original['text'])
        self.assertEqual(left['atom_sha256'],right['atom_sha256'])

    def test_linked_group_does_not_lose_records(self):
        groups=Groups([1,2,3,4,5])
        groups.union(2,3);groups.union(1,2);groups.union(4,5)
        self.assertEqual([groups.find(i) for i in range(1,6)],[1,1,1,4,4])

    def test_uncertainty_and_partial_context_are_preserved(self):
        self.assertEqual(aggregate_routes(['low_priority']), 'low_priority')
        self.assertEqual(aggregate_routes(['low_priority'],False),'fetch_evidence')
        self.assertEqual(aggregate_routes(['low_priority','low_priority']),'fetch_evidence')
        self.assertEqual(aggregate_routes(['deep_read','fetch_evidence'],False),'deep_read')

    def test_novelty_question_contains_its_own_checklist(self):
        q=questions()
        self.assertEqual(len(q['novelty']['instructions']['existing_properties']),24)
        self.assertEqual(len(q['closest_existing']['criteria']),25)

    def test_response_uses_pinned_model_and_closed_choices(self):
        q=questions()
        result={'model':MODEL,'answers':{k:{'type':'choice','choice':next(iter(v['criteria']))} for k,v in q.items()},'usage':{'input_tokens':20,'output_tokens':10}}
        validate(result,q)
        result['model']='unexpected'
        with self.assertRaises(ValueError):validate(result,q)

if __name__=='__main__':unittest.main()
