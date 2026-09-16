%------------------------------------------------------------------------------
% File     : ARI606_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : For monotonic f, 2<=5 implies f(2)<=f(5), thus f(f(2)<=f(f(5))
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.3.0, 0.12 v7.1.0, 0.00 v6.2.0, 0.20 v6.1.0, 0.22 v6.0.0, 0.25 v5.5.0, 0.38 v5.4.0, 0.50 v5.3.0, 0.43 v5.2.0, 0.40 v5.1.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    3 (   0 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    2 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   2  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   5 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :    7 (   3 atm;   0 fun;   2 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    3 (   1 usr;   2 con; 0-1 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(f_type,type,
    f: $int > $int ).

tff(f_mon_implies_ff2_gt_ff5,conjecture,
    ( ! [X: $int,Y: $int] :
        ( $lesseq(X,Y)
       => $lesseq(f(X),f(Y)) )
   => $lesseq(f(f(2)),f(f(5))) ) ).

%------------------------------------------------------------------------------
