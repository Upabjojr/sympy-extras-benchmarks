%------------------------------------------------------------------------------
% File     : ARI535_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Integer: Stickel's arithmetic challenge
% Version  : Especial.
% English  : 

% Refs     : [Sti10] Stickel (2010), Email to G. Sutcliffe
% Source   : [Sti10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v6.2.0, 0.40 v6.1.0, 0.44 v6.0.0, 0.50 v5.4.0, 0.38 v5.3.0, 0.43 v5.2.0, 0.60 v5.1.0, 0.75 v5.0.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    2 (   0 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   4 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    8 (   0 atm;   2 fun;   4 num;   2 var)
%            Number of types       :    2 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    3 (   1   >;   2   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   1 usr;   0 prp; 3-3 aty)
%            Number of functors    :    3 (   0 usr;   1 con; 0-2 aty)
%            Number of variables   :    2 (   0   !;   2   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : 
%------------------------------------------------------------------------------
tff(p_type,type,
    p: ( $int * $int * $int ) > $o ).

tff(a,conjecture,
    ? [X: $int,Y: $int] :
      ( p(2,Y,$sum(2,Y))
     => p(X,2,$product(X,2)) ) ).

%------------------------------------------------------------------------------
