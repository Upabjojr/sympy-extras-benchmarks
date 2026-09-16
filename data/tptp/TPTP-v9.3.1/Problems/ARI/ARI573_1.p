%------------------------------------------------------------------------------
% File     : ARI573_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Three inequations imply a fourth one
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.4.0, 0.17 v7.3.0, 0.12 v7.1.0, 0.17 v7.0.0, 0.00 v6.1.0, 0.22 v6.0.0, 0.25 v5.5.0, 0.38 v5.4.0, 0.25 v5.3.0, 0.43 v5.2.0, 0.60 v5.1.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    4 (   0 equ)
%            Maximal formula atoms :    4 (   4 avg)
%            Number of connectives :    3 (   0   ~;   0   |;   2   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    7 (   7 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :   25 (   4 atm;  11 fun;   7 num;   3 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    5 (   0 usr;   2 con; 0-2 aty)
%            Number of variables   :    3 (   3   !;   0   ?;   3   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(impl_3_ineq,conjecture,
    ! [X: $int,Y: $int,Z: $int] :
      ( ( $lesseq(1,$sum($product(X,2),$uminus(Y)))
        & $lesseq(1,$sum($product(Y,2),$uminus(Z)))
        & $lesseq(1,$sum($product(Z,2),$uminus(X))) )
     => $lesseq(2,$sum($sum(X,Y),Z)) ) ).

%------------------------------------------------------------------------------
