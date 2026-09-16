%------------------------------------------------------------------------------
% File     : ARI599_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Inequations imply a = b, hence f(a,b) = f(b,a)
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v9.1.0, 0.25 v9.0.0, 0.12 v7.5.0, 0.10 v7.4.0, 0.00 v6.3.0, 0.29 v6.2.0, 0.50 v6.1.0, 0.44 v6.0.0, 0.43 v5.5.0, 0.56 v5.4.0, 0.50 v5.2.0, 0.83 v5.1.0
% Syntax   : Number of formulae    :    4 (   0 unt;   3 typ;   0 def)
%            Number of atoms       :    3 (   1 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    2 (   0   ~;   0   |;   1   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   3 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :   10 (   2 atm;   4 fun;   4 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    2 (   1   >;   1   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    6 (   3 usr;   4 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(a_type,type,
    a: $int ).

tff(b_type,type,
    b: $int ).

tff(f_type,type,
    f: ( $int * $int ) > $int ).

tff(ineq_imply_f_eq_f,conjecture,
    ( ( $lesseq($product(2,a),$product(2,b))
      & $lesseq($product(3,b),$product(3,a)) )
   => ( f(a,b) = f(b,a) ) ) ).

%------------------------------------------------------------------------------
