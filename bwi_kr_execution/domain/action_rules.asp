#const self = 1.

#program step(n).

% action navigate_to
is_near(self, T, n) :- navigate_to(T, n).
is_facing(self, T, n) :- navigate_to(T, n).
-is_near(self, F, n) :- navigate_to(T, n), is_near(self, F, n - 1), T != F.
%for now assume everything is connected

% action find_person
is_located(P, L, n) :- find_person(P, L, n).
is_facing(self, P, n) :- find_person(P, L, n).
:- find_person(P, L, n), is_near(self, L, n - 1).
:- find_person(P, L, n), 0{can_be_located(P, L); is_located(P, L)}0.

% action pick_up
is_holding(self, O, n) :- pick_up(O, L, n).
-is_placed(O, L, n) :- pick_up(O, L, n).
-hand_empty(n) :- pick_up(O, L, n).
:- pick_up(O, L, n), not is_placed(O, L, n - 1).
:- pick_up(O, L, n), not is_facing(self, L, n - 1).
:- pick_up(O, L, n), not hand_empty(n - 1).
:- pick_up(O, L, n), not has_concept(O, "sensed"), has_concept(L, "scanned").

% action put_down
-is_holding(self, O, n) :- put_down(O, L, n).
is_placed(O, L, n) :- put_down(O, L, n).
hand_empty(n) :- put_down(O, L, n).
:- put_down(O, L, n), not is_facing(self, L, n - 1).
:- put_down(O, L, n), not is_holding(self, O, n - 1).

% action perceive_surface
scanned(L, n) :- perceive_surface(O, L, n).
is_placed(O, L, n) :- perceive_surface(O, L, n).
:- perceive_surface(O, L, n), can_be_placed(O, L).
:- perceive_surface(O, L, n), not is_facing(self, L, n - 1).
:- perceive_surface(O, L, n), scanned(L, n - 1).

% action hand_over
is_delivered(O, P, n) :- hand_over(O, P, n).
hand_empty(n) :- hand_over(O, P, n).
:- hand_over(O, P, n), not is_facing(self, P, n - 1).
:- hand_over(O, P, n), not is_holding(self, O, n - 1).

%%inertial rules
is_located(P, L, n) :- is_located(P, L, n - 1), not -is_located(P, L, n).
is_near(self, L, n) :- is_near(self, L, n - 1), not -is_near(self, L, n).
is_placed(O, L, n) :- is_placed(O, L, n - 1), not -is_placed(O, L, n).
scanned(L, n) :- scanned(L, n - 1).
is_holding(self, O, n) :- is_holding(self, O, n - 1), not -is_holding(self, O, n).
hand_empty(n) :- hand_empty(n - 1), not -hand_empty(n).
is_delivered(O, P, n) :- is_delivered(O, P, n - 1).

% allow passing concept name in goal query
is_near_name(self, L_name, n) :- is_near(self, L_id, n), name(L_id, L_name).
is_placed_concept(O_concept, L_concept, n) :- is_placed(O_id, L_id, n), has_concept(O_id, O_concept), has_concept(L_id, L_concept).
is_in_concept(O_concept, R_concept, n) :- is_placed(O_id, L, n), is_in(L, R_id), has_concept(O_id, O_concept), has_concept(R_id, R_concept).
is_delivered_concept(O_concept, P, n) :- is_delivered(O_id, P, n), has_concept(O_id, O_concept).
scanned_concept(L_concept, n) :- scanned(L_id, n), has_concept(L_id, L_concept).
is_holding_concept(self, O_concept, n) :- is_holding(self, O_id, n), has_concept(O_id, O_concept).

#program base.

is_a(C1, C3) :- is_a(C1, C2), is_a(C2, C3).
instance_of(O, C1) :- instance_of(O, C2), is_a(C2, C1). 
has_concept(O, C) :- instance_of(O, C_id), name(C_id, C).

%% Support non-fluent to fluent promotion for basic attributes

is_near(self, L, 0) :- is_near(self, L).
is_located(P, L, 0) :- is_located(P, L).
is_placed(O, L, 0) :- is_placed(O, L).
is_facing(self, P, 0) :- is_facing(self, P).
is_holding(self, O, 0) :- is_holding(self, O).
is_delivered(O, P, 0) :- is_delivered(O, P).
is_near_name(self, L_name, 0) :- is_near(self, L_id), name(L_id, L_name).
is_placed_concept(O_concept, L_concept, 0) :- is_placed(O_id, L_id), has_concept(O_id, O_concept), has_concept(L_id, L_concept).
is_in_concept(O_concept, R_concept, 0) :- is_placed(O_id, L), is_in(L, R_id), has_concept(O_id, O_concept), has_concept(R_id, R_concept).
is_delivered_concept(O_concept, P, 0) :- is_delivered(O_id, P), has_concept(O_id, O_concept).
scanned_concept(L_concept, 0) :- scanned(L_id, 0), has_concept(L_id, L_concept).
is_holding_concept(self, O_concept, 0) :- is_holding(self, O_id, 0), has_concept(O_id, O_concept).

scanned(S, 0) :- has_concept(S, "scanned").
hand_empty(0) :- has_concept(self, "empty_handed").

% Silence warnings
default_location(O, L) :- default_location(O, L).
is_facing(self, P) :- is_facing(self, P).
is_near(self, L) :- is_near(self, L).
is_holding(self, O) :- is_holding(self, O).
is_in(L, R) :- is_in(L, R).
is_placed(O, L) :- is_placed(O, L).
is_located(P, L) :- is_located(P, L).
is_delivered(O, P) :- is_delivered(O, P).
-is_located(P, L, n) :- -is_located(P, L, n).
can_be_located_concept(O, L, 0) :- can_be_located_concept(O, L, 0).
can_be_placed_concept(O, L, 0) :- can_be_placed_concept(O, L, 0).

can_be_located(P, L_id) :- can_be_located_concept(P, L_concept, 0), has_concept(L_id, "beacon"), has_concept(L_id, L_concept).
can_be_located(P, L) :- can_be_located_concept(P, R_concept, 0), has_concept(R_id, "room"), has_concept(R_id, R_concept), is_in(L, R_id), has_concept(L, "beacon"), has_concept(P, "person").

can_be_placed(O, L_id) :- can_be_placed_concept(O, L_concept, 0), has_concept(L_id, "placement"), has_concept(L_id, L_concept).
can_be_placed(O, L) :- can_be_placed_concept(O, R_concept, 0), has_concept(R_id, "room"), has_concept(R_id, R_concept), is_in(L, R_id), has_concept(L, "placement"), has_concept(O, "object").

can_be_placed(O_id, L_id) :- default_location(O_category_id, L_concept_id), is_a(O_id, O_concept_id), is_a(O_concept_id, O_category_id), is_a(L_id, L_concept_id), has_concept(O_id, "hypothetical"), 0{can_be_placed_concept(O_id, L, 0)}0.

