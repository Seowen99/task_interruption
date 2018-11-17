#include <incmode>.
#program step(n).

1{
navigate_to(T, n) : has_concept(T, "location"); % TODO: change this to navigable
pick_up(O, L, n) : has_concept(O, "object"), has_concept(L, "placement"); % TODO: change object to graspable
put_down(O, L, n) : has_concept(O, "object"), has_concept(L, "placement");
hand_over(O, P, n) : has_concept(O, "object"), has_concept(P, "person");
perceive_surface(O, L, n) : has_concept(O, "object"), has_concept(L, "placement");
find_person(P, L, n) : has_concept(P, "person"), has_concept(L, "beacon")
}1.

#show navigate_to/2.
#show pick_up/3.
#show put_down/3.
#show hand_over/3.
#show perceive_surface/3.
#show find_person/3.