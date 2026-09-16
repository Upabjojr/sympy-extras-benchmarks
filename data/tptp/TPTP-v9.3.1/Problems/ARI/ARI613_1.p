%------------------------------------------------------------------------------
% File     : ARI613_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : There is an X > 3 and a Y < 1 whose sum is 0
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v7.5.0, 0.30 v7.4.0, 0.12 v7.3.0, 0.00 v6.3.0, 0.14 v6.2.0, 0.50 v6.1.0, 0.56 v6.0.0, 0.57 v5.5.0, 0.44 v5.4.0, 0.62 v5.3.0, 0.60 v5.2.0, 0.50 v5.1.0
% Syntax   : Number of formulae    :    3 (   0 unt;   2 typ;   0 def)
%            Number of atoms       :    7 (   1 equ)
%            Maximal formula atoms :    7 (   7 avg)
%            Number of connectives :    6 (   0   ~;   0   |;   3   &)
%                                         (   0 <=>;   3  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    6 (   6 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :   10 (   2 atm;   1 fun;   3 num;   4 var)
%            Number of types       :    2 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    2 (   2   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    4 (   2 usr;   0 prp; 1-2 aty)
%            Number of functors    :    4 (   0 usr;   3 con; 0-2 aty)
%            Number of variables   :    4 (   2   !;   2   ?;   4   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(p_type,type,
    p: $int > $o ).

tff(q_type,type,
    q: $int > $o ).

tff(interv_3_infty_and_neginfty_1_contain_compl,conjecture,
    ( ( ! [X: $int] :
          ( $less(3,X)
         => p(X) )
      & ! [X: $int] :
          ( $less(X,1)
         => q(X) ) )
   => ? [X: $int,Y: $int] :
        ( p(X)
        & q(Y)
        & ( $sum(X,Y) = 0 ) ) ) ).

%------------------------------------------------------------------------------
