%------------------------------------------------------------------------------
% File     : ARI600_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Inequations imply a+1 = b-1, hence f(a+1,b-1) <= f(b-1,a+1) + 1
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : CounterSatisfiable
% Rating   : 0.00 v9.3.0, 0.33 v8.2.0, 0.00 v6.3.0, 0.50 v6.2.0, 0.40 v6.1.0, 0.67 v6.0.0, 0.75 v5.3.0, 0.71 v5.2.0, 1.00 v5.1.0
% Syntax   : Number of formulae    :    4 (   0 unt;   3 typ;   0 def)
%            Number of atoms       :    3 (   0 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    2 (   0   ~;   0   |;   1   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   3 avg)
%            Maximal term depth    :    4 (   2 avg)
%            Number arithmetic     :   17 (   3 atm;   7 fun;   7 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    2 (   1   >;   1   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    7 (   3 usr;   4 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_CSA_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(a_type,type,
    a: $int ).

tff(b_type,type,
    b: $int ).

tff(f_type,type,
    f: ( $int * $int ) > $int ).

tff(ineq_imply_f_leq_fplus1,conjecture,
    ( ( $lesseq(a,$sum(b,2))
      & $lesseq(b,$difference(a,2)) )
   => $lesseq(f($sum(a,1),$difference(b,1)),$sum(1,f($difference(b,1),$sum(a,1)))) ) ).

%------------------------------------------------------------------------------
