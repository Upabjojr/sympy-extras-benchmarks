%------------------------------------------------------------------------------
% File     : ARI601_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : If f(X) > X, then 3 < a implies 4 < a+1 < f(a+1)
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.3.0, 0.12 v7.1.0, 0.00 v6.2.0, 0.20 v6.1.0, 0.33 v6.0.0, 0.38 v5.4.0, 0.62 v5.3.0, 0.57 v5.2.0, 0.80 v5.1.0
% Syntax   : Number of formulae    :    3 (   0 unt;   2 typ;   0 def)
%            Number of atoms       :    3 (   0 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    2 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   2  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   3 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :    8 (   3 atm;   1 fun;   3 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    6 (   2 usr;   4 con; 0-2 aty)
%            Number of variables   :    1 (   1   !;   0   ?;   1   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(a_type,type,
    a: $int ).

tff(f_type,type,
    f: $int > $int ).

tff(fX_gt_X_implies_ineq,conjecture,
    ( ! [X: $int] : $greater(f(X),X)
   => ( $less(3,a)
     => $less(4,f($sum(a,1))) ) ) ).

%------------------------------------------------------------------------------
