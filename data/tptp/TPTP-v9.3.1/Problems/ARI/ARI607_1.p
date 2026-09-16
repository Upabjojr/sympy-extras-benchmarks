%------------------------------------------------------------------------------
% File     : ARI607_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : For monotonic f, f(2) <= f(3) and f(5) <= f(7), hence the sum
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.3.0, 0.12 v7.1.0, 0.17 v7.0.0, 0.00 v6.2.0, 0.20 v6.1.0, 0.33 v6.0.0, 0.38 v5.4.0, 0.62 v5.3.0, 0.57 v5.2.0, 0.80 v5.1.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    3 (   0 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    2 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   2  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   5 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :   11 (   3 atm;   2 fun;   4 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    6 (   1 usr;   4 con; 0-2 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(f_type,type,
    f: $int > $int ).

tff(f_mon_implies_f2plusf5_gt_f7plusf3,conjecture,
    ( ! [X: $int,Y: $int] :
        ( $lesseq(X,Y)
       => $lesseq(f(X),f(Y)) )
   => $lesseq($sum(f(2),f(5)),$sum(f(7),f(3))) ) ).

%------------------------------------------------------------------------------
